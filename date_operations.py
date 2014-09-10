from pytz import timezone
from datetime import datetime

# interval in minutes
def date_interval(compared_date, interval):
    now = datetime.now(timezone('UTC'))
    compared_date = datetime.strptime(compared_date, "%Y-%m-%dT%H:%M:%SZ")
    compared_date = compared_date.replace(tzinfo=timezone('UTC'))

    return (now - compared_date).total_seconds() >= (int(interval) * 60)
