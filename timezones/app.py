from flask import Flask, render_template, request
from datetime import datetime
import pytz
import requests
import os

app = Flask(__name__)

TIMEZONES = pytz.common_timezones


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        time_str = request.form.get('time')
        base_tz = request.form.get('base_tz') or 'UTC'
        # validate base timezone; fall back to UTC if invalid
        try:
            base_tz_obj = pytz.timezone(base_tz)
        except Exception:
            base_tz = 'UTC'
            base_tz_obj = pytz.timezone(base_tz)
        # collect target entries (either timezone IDs or city/place strings)
        targets = [t.strip() for t in request.form.getlist('targets') if t and t.strip()]

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

        # resolve targets into header label/tz pairs
        # headers will be list of (label, tzname_or_none)
        # collect multiple times; empty entries will be treated as 'now' when processing
        times_raw = request.form.getlist('times')
        if not times_raw:
            times_raw = [request.form.get('time', '')]

        # prepare list of base datetimes (one per input time)
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

        # build headers: base timezone first, then each target (resolve timezone or city)
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

        # build matrix rows: each row corresponds to an input time
        rows_matrix = []
        for base_dt in base_datetimes:
            # display input time without timezone information
            base_display = base_dt.strftime('%Y-%m-%d %H:%M:%S')
            row_cells = []
            for label, tzname in headers:
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

        header_labels = [h[0] for h in headers]
        return render_template('results.html', headers=header_labels, rows=rows_matrix)

    return render_template('index.html', timezones=TIMEZONES)


if __name__ == '__main__':
    app.run(debug=True)
