#!/usr/bin/env python3
"""adding timezones"""


from flask_babel import timezone
import pytz


@babel.timezoneselector
def get_timezone():
    """timezone function"""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    user = getattr(g, 'user', None)
    if user:
        try:
            return pytz.timezone(user.get('timezone')).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return 'UTC'
