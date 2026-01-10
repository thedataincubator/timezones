import pytest

import pytz
from datetime import datetime
import conversions

def test_simple_conversion():
    # This is avoiding city lookup
    # making sure conversion to timezone objects occurs
    base_tz = 'US/Eastern'
    targets = ['US/Pacific', 'Europe/London']
    base_tz_obj = pytz.timezone(base_tz)

    dt = datetime.fromisoformat('2025-12-10T12:00:00')
    times = [base_tz_obj.localize(dt)]

    matrix = conversions.convert_times(times, targets)
    assert matrix == [('2025-12-10 12:00:00', ['2025-12-10 09:00:00', '2025-12-10 17:00:00'])]
    

