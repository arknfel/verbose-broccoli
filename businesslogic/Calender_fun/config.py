from common.root_aggregate import Config


class CalendarEventActorConfigError(Config.error_type): ...


class CalendarEventActorConfig(Config):
    error_type = CalendarEventActorConfigError

    @property
    def rule_name_prefix(self):
        return self.get('rule_name_prefix', 'cal_event')

    @property
    def calendar_url(self):
        return self.get('calendar_url')

    @property
    def timezone(self):
        return self.get('timezone', 'Europe/Berlin')

    @property
    def date_format(self):
        return self.get('dateformat', r'%Y-%m-%d %H:%M')

    @property
    def clean_eventname_config(self):
        return self.get('clean_eventname_config', {'replacement_regex': r'[ ()-]', 'char': '_'})

    @property
    def expirydate_offset(self):
        return self.get('expiry_date_offset')

    def validate(self):
        if not self.calendar_url:
            raise self.error_type("Missing or null 'calendar_url'")
