import requests
import pytz
import os
from datetime import datetime

# Converts a city/place name to a timezone ID using geonames
# Since geonames takes lat/lon, we first use Nominatim to get coordinates
# returns None if it can't get the timezone
def resolve_city_to_tz(city_name):
    try:
        params = {'q': city_name, 'format': 'json', 'limit': 1}
        resp = requests.get('https://nominatim.openstreetmap.org/search', params=params, headers={'User-Agent': 'VibeTZ/1.0'})
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        lat = data[0].get('lat')
        lon = data[0].get('lon')
        if not lat or not lon:
            return None
        username = os.getenv('GEONAMES_USERNAME', 'demo')
        tz_resp = requests.get(f'http://api.geonames.org/timezoneJSON?lat={lat}&lng={lon}&username={username}')
        tz_resp.raise_for_status()
        tz_data = tz_resp.json()
        tzid = tz_data.get('timezoneId')
        return tzid
    except Exception:
        return None
    
def get_column_headers(base_tz, targets):
    headers = [(base_tz, base_tz)]
    for t in targets:
        # try interpreting target as a timezone id first
        tzname = None
        label = None
        try:
            pytz.timezone(t)
            tzname = t
            label = t
        except Exception:
            # treat as city/place and attempt to resolve
            tzid = resolve_city_to_tz(t)
            if tzid:
                tzname = tzid
                label = f"{t} ({tzid})"
            else:
                tzname = None
                label = f"{t} (Unrecognized)"

        # avoid duplicates by label and tz
        if label and label not in [h[0] for h in headers]:
            headers.append((label, tzname))

    return headers

def times_to_datetimes(base_tz_obj, times_raw):
    # prepare list of base datetimes (one per input time)
    # blank lines/empty boxes are ignored
    base_datetimes = []
    for t in times_raw:
        if not t or not t.strip():
            base_datetimes.append(datetime.now(base_tz_obj))
            continue
        try:
            dt = datetime.fromisoformat(t)
        except Exception:
            dt = datetime.strptime(t, "%Y-%m-%dT%H:%M")
        base_datetimes.append(base_tz_obj.localize(dt))

    return base_datetimes

def convert_times(base_datetimes, timezones):
    rows_matrix = []
    for base_dt in base_datetimes:
        # display input time without timezone information
        base_display = base_dt.strftime('%Y-%m-%d %H:%M:%S')
        row_cells = []
        for tzname in timezones:
            if not tzname:
                row_cells.append('Unrecognized location')
                continue
            try:
                tz_obj = pytz.timezone(tzname)
                converted = base_dt.astimezone(tz_obj)
                # show only date and time in the grid cells
                row_cells.append(converted.strftime('%Y-%m-%d %H:%M:%S'))
            except Exception:
                row_cells.append('Unrecognized timezone')
        rows_matrix.append((base_display, row_cells))

    return rows_matrix
