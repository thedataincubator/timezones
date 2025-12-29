# Timezones Flask App

Simple Flask app that converts a list of times to multiple time zones.

For the city lookup to work properly, you'll need an account at https://www.geonames.org/ (it's free, but make sure that you enable access to the free API in your account settings). You don't need an API key, just your username.

Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r timezones/requirements.txt
export FLASK_APP=timezones/app.py
export export GEONAMES_USERNAME=<yourusername>
flask run
```

Open http://127.0.0.1:5000/ and use the form.
