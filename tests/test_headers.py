from unittest.mock import patch

from conversions import get_column_headers

# Mock out the API calls to figure out time zones.
def mock_city_to_tz(city):
    mapping = {
        'London': 'Europe/London',
        'Boston': 'US/Eastern',
        'New York': 'US/Eastern',
        'Baltimore': 'US/Eastern',
    }
    return mapping.get(city, None)

@patch('conversions.resolve_city_to_tz')
def test_headers(mock_resolve_city_to_tz):
    mock_resolve_city_to_tz.side_effect = mock_city_to_tz

    base_tz = 'UTC'
    targets = ['US/Eastern', 'London', 'InvalidCity', 'Asia/Tokyo']

    headers = get_column_headers(base_tz, targets)

    expected_headers = [
        ('UTC', 'UTC'),
        ('US/Eastern', 'US/Eastern'),
        ('London (Europe/London)', 'Europe/London'),
        ('InvalidCity (Unrecognized)', None),
        ('Asia/Tokyo', 'Asia/Tokyo')
    ]

    assert headers == expected_headers

@patch('conversions.resolve_city_to_tz')
def test_duplicate_headers(mock_resolve_city_to_tz):
    """Check that we only show each city / TZ once in the headers."""
    mock_resolve_city_to_tz.side_effect = mock_city_to_tz

    base_tz = 'UTC'
    targets = ['US/Eastern', 'US/Eastern', 'US/Eastern']

    headers = get_column_headers(base_tz, targets)

    assert len(headers) == 1
