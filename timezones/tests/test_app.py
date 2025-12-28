import pytest

from timezones.app import app


class MockResp:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self._data


def test_home_page():
    client = app.test_client()
    r = client.get('/')
    assert r.status_code == 200
    assert b'Convert times across timezones' in r.data or b'Convert times' in r.data


def test_convert_timezone_id():
    client = app.test_client()
    data = {
        'times': '2025-12-28T15:30',
        'base_tz': 'UTC',
        'targets': 'Europe/London'
    }
    r = client.post('/', data=data)
    assert r.status_code == 200
    # base time should appear (localized to UTC) and header should include the tz
    assert b'2025-12-28 15:30:00' in r.data
    assert b'Europe/London' in r.data


def test_city_resolution(monkeypatch):
    def fake_get(url, params=None, headers=None):
        if 'nominatim.openstreetmap.org' in url:
            return MockResp([{'lat': '19.0759899', 'lon': '72.8773928'}])
        if 'geonames.org' in url:
            return MockResp({'timezoneId': 'Asia/Kolkata'})
        raise RuntimeError('Unexpected URL: ' + str(url))

    monkeypatch.setattr('requests.get', fake_get)

    client = app.test_client()
    data = {'times': '2025-12-28T12:00', 'base_tz': 'UTC', 'targets': 'Mumbai, India'}
    r = client.post('/', data=data)
    assert r.status_code == 200
    assert b'Mumbai (Asia/Kolkata)' in r.data
