import os
from datetime import datetime
import pytz
import requests
from flask import Flask, render_template, request
from conversions import *


app = Flask(__name__)

TIMEZONES = pytz.common_timezones


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        base_tz = request.form.get('base_tz') or 'UTC'
        # validate base timezone; fall back to UTC if invalid
        try:
            base_tz_obj = pytz.timezone(base_tz)
        except Exception:
            base_tz = 'UTC'
            base_tz_obj = pytz.timezone(base_tz)

        # collect target entries (either timezone IDs or city/place strings)
        targets = [t.strip() for t in request.form.getlist('targets') if t and t.strip()]

        # collect multiple times; empty entries will be treated as 'now' when processing
        times_raw = request.form.getlist('times')
        if not times_raw:
            times_raw = [request.form.get('time', '')]

        # prepare list of base datetimes (one per input time)
        # ignores blank lines
        base_datetimes = times_to_datetimes(base_tz_obj, times_raw)

        # resolve targets into header label/tz pairs
        # build headers: base timezone first, then each target (resolve timezone or city)
        # headers will be list of (label, tzname_or_none)
        headers = get_column_headers(base_tz, targets)
        target_timezones = [head[1] for head in headers]

        # build matrix rows: each row corresponds to an input time
        # each column to a timezone (first will be base timezone)
        rows_matrix = convert_times(base_datetimes, target_timezones)

        header_labels = [h[0] for h in headers]

        # render back to the index page with results; keep submitted values to prefill the form
        return render_template('index.html', timezones=TIMEZONES, headers=header_labels, rows=rows_matrix, times=times_raw, targets=targets, base_tz=base_tz)

    # on GET show empty form (provide defaults for template)
    return render_template('index.html', timezones=TIMEZONES, times=[], targets=[], base_tz='')


if __name__ == '__main__':
    app.run(debug=True)
