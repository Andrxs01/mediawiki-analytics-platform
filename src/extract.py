import requests
import pandas as pd
from datetime import datetime, timedelta


LANGUAGES = [
    "es.wikipedia",
    "en.wikipedia",
    "fr.wikipedia",
    "de.wikipedia",
    "pt.wikipedia"
]


def get_top_articles(project, year, month, day):

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/"
        f"top/{project}/all-access/{year}/{month:02d}/{day:02d}"
    )

    headers = {
        "User-Agent": "MediaWikiAnalytics/1.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()

    rows = []

    for article in data["items"][0]["articles"]:

        rows.append({
            "timestamp": f"{year}-{month:02d}-{day:02d}",
            "project": project,
            "page_title": article["article"],
            "count_views": article["views"]
        })

    return rows
def extract_last_days(days=30):

    all_rows = []

    today = datetime.now()

    for i in range(days):

        date = today - timedelta(days=i)

        for project in LANGUAGES:

            try:

                rows = get_top_articles(
                    project,
                    date.year,
                    date.month,
                    date.day
                )

                all_rows.extend(rows)

                print(
                    f"OK {project} {date.date()}"
                )

            except Exception as e:

                print(
                    f"ERROR {project} {date.date()} {e}"
                )

    return pd.DataFrame(all_rows)