# VibeTZ — Timezone converter (Flask)

A small Flask web app that converts one or more input times into multiple time zones (by IANA timezone ID or city/place name). City/place lookups are resolved server-side on submit using a geocoder + GeoNames timezone service.

## Features

- Convert multiple input times at once.
- Enter targets as either IANA timezone IDs (e.g. `America/Los_Angeles`) or place names (e.g. `San Francisco, CA`).
- Minimal JavaScript UI with add/remove inputs and datalist autocompletion.
- Server-side city → timezone resolution (Nominatim geocoding + GeoNames timezone lookup).

## How to Use the App

1. Enter one or more times in the left column (the app accepts `YYYY-MM-DD HH:MM` or similar ISO-like inputs).
2. Choose a base timezone (you can type to filter) — this is the timezone of the input times.
3. Add one or more target entries in the right column; each target can be either an IANA timezone (e.g., `Europe/London`) or a city/place name (e.g., `Mumbai, India`).
4. Submit the form to see a grid of converted times. Each cell shows the converted date/time in that timezone.

Tips:

- Use an exact IANA timezone ID when possible for predictable results.
- If a place lookup is ambiguous, try adding a region/country (e.g., `Springfield, IL` vs `Springfield, MA`).

## Quick Start

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/RichardOtt/VibeTZ?quickstart=1)


1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r timezones/requirements.txt
```

3. Set environment variables and run the app (Unix/macOS):

```bash
export FLASK_APP=timezones/app.py
export FLASK_ENV=development
export GEONAMES_USERNAME=your_geonames_username
flask run
```

On Windows (PowerShell):

```powershell
$env:FLASK_APP = 'timezones/app.py'
$env:FLASK_ENV = 'development'
$env:GEONAMES_USERNAME = 'your_geonames_username'
flask run
```

3. Alternative: you can also run the app with
```bash
export GEONAMES_USERNAME=your_geonames_username
cd timezones
python app.py
```

Open http://127.0.0.1:5000/ in your browser.

## Geonames & City Lookup

The app uses two free services to resolve place names to timezones:

- Nominatim (OpenStreetMap) for geocoding (place → lat/lon).
- GeoNames `timezoneJSON` service for lat/lon → IANA timezone.

GeoNames requires a username. Create a free account at https://www.geonames.org/ and set the `GEONAMES_USERNAME` environment variable before running the app. You'll also need to activate the free API on your account. The app will fall back to the GeoNames `demo` username if you don't set one, but that account is strictly rate-limited and not suitable for production.

Notes and best practices:

- Respect Nominatim's usage policy: do not bulk-query their service and add a sensible delay or caching for repeated lookups. See https://operations.osmfoundation.org/policies/nominatim/.
- Use your own GeoNames username to avoid the `demo` quota.



## Project Structure

- `timezones/app.py`: Flask application (routes, form handling, timezone and city-resolution logic).
- `timezones/templates/index.html`: Main page with the input form and inline results.
- `timezones/requirements.txt`: Python dependencies.
- `timezones/tests/test_app.py`: Pytest tests (external HTTP calls are mocked for determinism).
- `timezones/README.md`: This file.

## Troubleshooting

- Time format issues: the app expects reasonably parseable datetimes. If your input is rejected or parsed incorrectly, try using full `YYYY-MM-DD HH:MM` format.
- Unrecognized timezone: If you enter an invalid timezone ID you'll see an "Unrecognized timezone" message in results. Use an IANA timezone ID (see the Olson database, for example https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for best results.
- City lookup failures: If a place name doesn't resolve, try these steps:
  - Add more context (city, state/province, country).
  - Confirm `GEONAMES_USERNAME` is set and valid.
  - Check network connectivity and that external services are reachable.
  - Consider switching to a timezone ID directly to bypass geocoding.
- Rate limiting: If many lookups are done in a short time you may hit Nominatim or GeoNames rate limits. Add caching, batch requests, or run fewer queries during development.

## Running Tests

Install the test extras (already covered by `requirements.txt`) and run:

```bash
pytest -q
```

Tests mock external HTTP calls so they should run without network access.

## Notes for Deploying / Production

- Replace the `demo` GeoNames username with your own and implement caching for geocoding results.
- If you expect heavy traffic, set up a private geocoding/timezone service or use a commercial provider to avoid rate limits.
- Serve the Flask app with a production WSGI server (Gunicorn / uWSGI) behind a reverse proxy.



