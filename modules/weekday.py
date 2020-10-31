import requests
import json

api_url = "http://ukenummer.no/json"

def fetch_weekday():
    try:
        r = requests.get(api_url)
        response = json.loads(r.text)
        dates = response["dates"]
        return "Week: {}  ->  From {} to {}".format(response["weekno"], dates["fromdate_iso"], dates["todate_iso"])
    except Exception as e:
        print("Failed to fetch weekday:", e)
        return "Something went wrong when getting weekday. Try again later or contact my creator."

