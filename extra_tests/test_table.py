from bs4 import BeautifulSoup

# We can use this for either a broken test (by changing div.mt-4 to div.mt-5)
# or to do self-healing by having it react to that change. Or both.
def test_index_html_table():
    from app import app

    with app.test_client() as client:
        data = {
            'times': ['2025-12-10T12:00:00', '2025-12-11T13:30:00'],
            'targets': ['US/Pacific', 'Europe/London'],
            'base_tz': 'US/Eastern'
        }
        resp = client.post('/', data=data)
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)

    with open("example_out.html", "w") as f:
        f.write(html)
    soup = BeautifulSoup(html, 'html.parser')
    dates = soup.select('div.mt-3 tr td div')
    assert len(dates) == 6
    expected_dates = [
        '2025-12-10 12:00:00',
        '2025-12-10 09:00:00',
        '2025-12-10 17:00:00',
        '2025-12-11 13:30:00',
        '2025-12-11 10:30:00',
        '2025-12-11 18:30:00'
    ]
    date_str = [d.get_text(strip=True) for d in dates]
    assert date_str == expected_dates