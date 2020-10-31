import requests as rq
import json

#rq = rq.get("https://jesusapi.000webhostapp.com/api")
#rq.text

#print(rq.text)

def trump():
    try:
        url = 'https://tronalddump.io/random/quote'
        response = rq.get(url)
        response_json = json.loads(response.content)
        return "Trump: " + response_json.get('value')
    except:
        return "I'm a perfect physical specimen!"


