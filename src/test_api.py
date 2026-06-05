import requests
import json

URL = (
    "https://wikimedia.org/api/rest_v1/metrics/pageviews/"
    "top/es.wikipedia/all-access/2026/04/01"
)

headers = {
    "User-Agent": "MediaWikiAnalytics/1.0"
}

response = requests.get(URL, headers=headers)

data = response.json()

print(json.dumps(data["items"][0], indent=4))