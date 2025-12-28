from flask import Flask, render_template, request
from datetime import datetime
import pytz

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
        # collect target zones, ignore empty inputs
        zones = [z.strip() for z in request.form.getlist('zones') if z and z.strip()]
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

        # build columns (timezones) with base_tz first, avoid duplicates
        cols = [base_tz]
        for z in zones:
            if z and z != base_tz and z not in cols:
                cols.append(z)

        # build matrix rows: each row corresponds to an input time
        rows_matrix = []
        for base_dt in base_datetimes:
            # display input time without timezone information
            base_display = base_dt.strftime('%Y-%m-%d %H:%M:%S')
            row_cells = []
            for col in cols:
                try:
                    tz_obj = pytz.timezone(col)
                    converted = base_dt.astimezone(tz_obj)
                    # show only date and time in the grid cells
                    row_cells.append(converted.strftime('%Y-%m-%d %H:%M:%S'))
                except Exception:
                    row_cells.append('Unrecognized timezone')
            rows_matrix.append((base_display, row_cells))

        return render_template('results.html', headers=cols, rows=rows_matrix)

    return render_template('index.html', timezones=TIMEZONES)


if __name__ == '__main__':
    app.run(debug=True)
