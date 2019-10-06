from requests import get
import json

def todays_names(line):
    url = "https://api.abalin.net/get/today?country=us"
    try:
        raw_json = get(url).text
        parsed_json = json.loads(raw_json) 
        names = parsed_json.get("data").get("name_us")
        return "Today's Names: " + names
    except:
        return "Something went wrong.."
     
