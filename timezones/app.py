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

        if not time_str:
            base_dt = datetime.now(base_tz_obj)
        else:
            # datetime-local input like '2025-12-28T15:30'
            try:
                dt = datetime.fromisoformat(time_str)
            except Exception:
                dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
            base_dt = base_tz_obj.localize(dt)

        results = []
        for z in zones:
            try:
                tz_obj = pytz.timezone(z)
            except Exception:
                # include an informative row for unknown timezone strings
                results.append((z, 'Unrecognized timezone'))
                continue
            converted = base_dt.astimezone(tz_obj)
            results.append((z, converted.strftime('%Y-%m-%d %H:%M:%S %Z%z')))

        return render_template('results.html', base_dt=base_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'), results=results, base_tz=base_tz)

    return render_template('index.html', timezones=TIMEZONES)


if __name__ == '__main__':
    app.run(debug=True)
