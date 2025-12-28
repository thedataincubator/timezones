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
        zones = request.form.getlist('zones')

        if not time_str:
            base_dt = datetime.now(pytz.timezone(base_tz))
        else:
            # datetime-local input like '2025-12-28T15:30'
            try:
                dt = datetime.fromisoformat(time_str)
            except Exception:
                dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
            base_dt = pytz.timezone(base_tz).localize(dt)

        results = []
        for z in zones:
            tz = pytz.timezone(z)
            converted = base_dt.astimezone(tz)
            results.append((z, converted.strftime('%Y-%m-%d %H:%M:%S %Z%z')))

        return render_template('results.html', base_dt=base_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'), results=results, base_tz=base_tz)

    return render_template('index.html', timezones=TIMEZONES)


if __name__ == '__main__':
    app.run(debug=True)
