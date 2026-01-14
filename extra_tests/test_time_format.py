from datetime import datetime
import pytz

from conversions import times_to_datetimes

def test_expected_format():
    input_times = ['2025-12-10T12:00:00', '2026-02-28T23:45:00']
    base_tz = 'US/Eastern'
    base_tz_obj = pytz.timezone(base_tz)
    output_times = [base_tz_obj.localize(datetime(2025, 12, 10, 12, 0, 0)), 
                    base_tz_obj.localize(datetime(2026, 2, 28, 23, 45, 0))]

    converted_times = times_to_datetimes(base_tz_obj, input_times)
    assert converted_times == output_times

# Rob: this one contains an error, the second time is 22:45 not 23:45
def test_blank_time():
    input_times = ['2025-12-10T12:00:00', '', '2026-02-28T22:45:00', '    ']
    base_tz = 'Europe/London'
    base_tz_obj = pytz.timezone(base_tz)
    output_times = [base_tz_obj.localize(datetime(2025, 12, 10, 12, 0, 0)), 
                    base_tz_obj.localize(datetime(2026, 2, 28, 23, 45, 0))]
    converted_times = times_to_datetimes(base_tz_obj, input_times)

    # blank times become the current time, so just check length and known entries
    assert len(converted_times) == 4
    assert converted_times[0] == output_times[0]
    assert converted_times[2] == output_times[1]

# Rob: this one triggers an actual bug - the code only handles ISO format
# should either switch to using dateutil, or some failure handling (time.now instead? skip?)
# the html form _can't_ give this, but someone can post and cause the app to fail
def test_other_format():
    input_times = ['2025-12-10 12:00:00', '2026/02/28T23:45:00']
    base_tz = 'US/Eastern'
    base_tz_obj = pytz.timezone(base_tz)
    output_times = [base_tz_obj.localize(datetime(2025, 12, 10, 12, 0, 0)), 
                base_tz_obj.localize(datetime(2026, 2, 28, 23, 45, 0))]

    converted_times = times_to_datetimes(base_tz_obj, input_times)
    assert converted_times == output_times