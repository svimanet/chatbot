import requests as rq
import json

#rq = rq.get("https://jesusapi.000webhostapp.com/api")
#rq.text

#print(rq.text)

def jesus():
    try:
        url = 'https://jesusapi.000webhostapp.com/api'
        response = rq.get(url)
        response_json = json.loads(response.text)
        return "Have a blessed day: " + response_json.get('link')
    except:
        return "Jesus says Good day!"


