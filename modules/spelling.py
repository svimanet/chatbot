import requests
import json

def check_spelling(sentence):
    spelling = sentence.split('!check ')[1].lower()
    sentence = spelling.replace(" ", "+")
    response = requests.get("https://montanaflynn-spellcheck.p.mashape.com/check/?text={}".format(spelling),
      headers={
        "X-Mashape-Key": "11SWTKGpRomshXZD5oHV4RUH1XAIp1SLSckjsnGDefU3k5Zfyd",
        "Accept": "application/json"
      }
    )
    response_json = json.loads(response.text)
    suggestion = response_json.get("suggestion").lower().split('.')[0]
    if str(suggestion).lower() in spelling:
        return("Looks good to me.")
    else:
        return("{}*".format(suggestion))
