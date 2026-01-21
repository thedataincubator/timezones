from datetime import datetime
import pytz

from conversions import times_to_datetimes

# Conversion to datetime objects works as expected for normal cases
def test_expected_format():
    input_times = ['2025-12-10T12:00', '2026-02-28T23:45']
    base_tz = 'US/Eastern'
    base_tz_obj = pytz.timezone(base_tz)
    output_times = [base_tz_obj.localize(datetime(2025, 12, 10, 12, 0)),
                    base_tz_obj.localize(datetime(2026, 2, 28, 23, 45))]

    converted_times = times_to_datetimes(base_tz_obj, input_times)
    assert converted_times == output_times

# Checking blank times (so empty boxes) become the current time
def test_blank_time():
    input_times = ['2025-12-10T12:00', '', '2026-02-28T22:45', '    ']
    base_tz = 'Europe/London'
    base_tz_obj = pytz.timezone(base_tz)
    output_times = [base_tz_obj.localize(datetime(2025, 12, 10, 12, 0)),
                    base_tz_obj.localize(datetime(2026, 2, 28, 23, 45))]
    converted_times = times_to_datetimes(base_tz_obj, input_times)

    # blank times become the current time, so just check length and known entries
    assert len(converted_times) == 4
    assert converted_times[0] == output_times[0]
    assert converted_times[2] == output_times[1]

# Checking that non-ISO formats are handled correctly
# HTML won't send this, but a direct POST could trigger it
def test_other_format():
    input_times = ['2025-12-10 12:00', '2026/02/28T23:45']
    base_tz = 'US/Eastern'
    base_tz_obj = pytz.timezone(base_tz)
    output_times = [base_tz_obj.localize(datetime(2025, 12, 10, 12)), 
                base_tz_obj.localize(datetime(2026, 2, 28, 23, 45))]

    converted_times = times_to_datetimes(base_tz_obj, input_times)
    assert converted_times == output_times