import logging
import time
import json

import arrow
import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_rules(logger: logging.Logger) -> list[dict]:
    logger.info(f'Initializing the "ResourceGroupsTaggingApi" client')
    client = boto3.client('resourcegroupstaggingapi', region_name='eu-central-1')
    filters = [{'Key': 'expiry_timestamp'}]
    logger.info(f'Getting resources, filters: {filters}')
    response = client.get_resources(TagFilters=filters)
    respurces_map = response['ResourceTagMappingList']
    logger.debug(json.dumps(response, indent=4))
    logger.info(json.dumps(respurces_map, indent=4))
    client.close()
    return respurces_map


def delete_expired_rules(logger: logging.Logger, rules: list, tz='Europe/Berlin'):
    expired = []
    logger.info(f'Initializing the "EventBridge" client')
    client = boto3.client('events', region_name='eu-central-1')
    ref_time = arrow.now(tz=tz)
    for rule in rules:
        rule_name = rule['ResourceARN'].split('/')[-1]
        rule_expiry_time = [d['Value'] for d in rule['Tags'] if d['Key'] == 'expiry_timestamp'].pop()
        if not bool(rule_expiry_time):
            logger.warn(f"Missing value for key \"expiry_timestamp\", skipping rule \"{rule['ResourceArn']}\"")
            continue
        if arrow.Arrow.fromtimestamp(float(rule_expiry_time), tzinfo=tz) <= ref_time:
            expired.append(rule_name)
            # breakpoint()
            ids = [target['Id'] for target in client.list_targets_by_rule(Rule=rule_name)['Targets']]
            if ids:
                logger.info(f'Removing targets of Rule "{rule_name}": {ids}')
                client.remove_targets(Rule=rule_name, Ids=ids)

    logger.info(json.dumps({f'expired': expired}))
    if expired:
        logger.info('Deleting expired rules')
        time.sleep(2)
        for rule_name in expired:
            client.delete_rule(Name=rule_name)
        time.sleep(2)


def lambda_handler(event: dict, context):
    rules_map = get_rules(logger)
    delete_expired_rules(logger, rules_map)
    logger.info('Done.')


if __name__ == "__main__":
    lambda_handler(None)
