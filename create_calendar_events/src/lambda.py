import logging
import requests
import json
import re

import arrow
from ics import Calendar

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CronRule:
    def __init__(self, logger: logging.Logger, name, cron_expr, state='ENABLED', client=None):
        self.client = boto3.client('events') if not client else client
        self.logger = logger
        self.name = name
        self.cron_expr = cron_expr
        self.state = state
        self.arn = None
        self.tags = []

    def create(self):
        self.arn = self.client.put_rule(Name=self.name, ScheduleExpression=self.cron_expr, State=self.state)[
            'RuleArn'
        ]
        return self

    def list_targets(self):
        return self.client.list_targets_by_rule(Rule=self.name)['Targets']

    def put_targets(self, targets):
        self.client.put_targets(Rule=self.name, Targets=targets)
        return self

    def remove_targets(self, ids):
        self.client.remove_targets(Rule=self.name, Ids=ids)
        return self

    def delete(self, force=False):
        target_ids = [target['Id'] for target in self.list_targets()]
        self.remove_targets(ids=target_ids)
        self.client.delete_rule(Name=self.name, Force=force)

    def tag(self, tags):
        if self.arn:
            self.client.tag_resource(ResourceARN=self.arn, Tags=tags)
        return self


def get_calendar_data(url):
    """
    Function downloads the calendar data of a given url,
    returns a list of 'Calendar' objects of the parsed data.
    """
    return Calendar.parse_multiple(
        '\n'.join([line for line in requests.get(url).text.split('\n') if not line.startswith('UID:')])
    )


def lambda_handler(event, context):
    logger.info(json.dumps({'event': event}))

    # Config
    _event: dict = event
    account_id = _event['account_id']
    region = _event['region']
    rule_prefix = _event.get('rule_prefix', 'cal_event')
    calendar_url = _event['calendar_url']
    timezone = _event.get('timezone', 'Europe/Berlin')
    date_format = _event.get('date_format', r'%Y-%m-%d %H:%M')
    name_regex = _event.get('name_regex', {'replacement_regex': r'[ ()-]', 'char': '_'})
    expirydate_offset = _event.get('expirydate_offset', 7)

    expiry_date = arrow.now(tz=timezone).shift(days=-expirydate_offset)

    logger.info(f'Fetchine calendar data at url:{calendar_url}')
    calenders = get_calendar_data(calendar_url)

    expired = []
    eligible = []
    events_created = []
    logger.info("Initializing client 'EventBridge'")
    eventbridge = boto3.client('events')
    # eventbridge = boto3.Session(profile_name='saml').client('events', region_name='eu-central-1')

    # Attribute templates
    rule_name = '{}_{}_{}'
    cron_expr = 'cron({} {} {} {} ? {})'
    lamda_arn = f'arn:aws:lambda:{region}:{account_id}:function:'

    for calendar in calenders:
        logger.info('Processing calendar events')
        for event in calendar.events:
            event_expirydate: arrow.Arrow = event.end.shift(days=expirydate_offset)
            named_as = re.sub(rf'{name_regex['replacement_regex']}', name_regex['char'], event.name)
            event_meta = {
                'name': event.name,
                'named_as': named_as,
                'start': event.begin.strftime(date_format),
                'end': event.end.strftime(date_format),
                'expiry': event_expirydate.strftime(date_format),
            }

            if event.end <= expiry_date:
                expired.append(event_meta)
                continue

            eligible.append(event_meta)

            tags = [{'Key': 'expiry_timestamp', 'Value': f'{event_expirydate.timestamp()}'}]

            # Create start rule
            label = 'start'
            _time = event.begin
            target_id = 'EC2_ondemand_' + label
            arn = lamda_arn + target_id

            rule = CronRule(
                logger,
                rule_name.format(rule_prefix, label, named_as),
                cron_expr.format(_time.minute, _time.hour, _time.day, _time.month, _time.year),
                client=eventbridge,
            )
            rule.create()
            rule.put_targets([{'Id': target_id, 'Arn': arn}])
            rule.tag(tags)

            # Create end rule
            label = 'end'
            _time = event.end
            target_id = 'EC2_ondemand_' + label
            arn = lamda_arn + target_id

            rule = CronRule(
                logger,
                rule_name.format(rule_prefix, label, named_as),
                cron_expr.format(_time.minute, _time.hour, _time.day, _time.month, _time.year),
                client=eventbridge,
            )
            rule.create()
            rule.put_targets([{'Id': target_id, 'Arn': arn}])
            rule.tag(tags)

            events_created.append(event_meta)

    logger.info(json.dumps({'expired': expired, 'eligible': eligible}))
    logger.info(json.dumps({'events_created': events_created}))
    logger.info('Done.')
