import requests
import json

def check_spelling(spelling):
    spelling = spelling.lower()
    sentence = spelling.replace(" ", "+")
    response = requests.get("https://montanaflynn-spellcheck.p.mashape.com/check/?text={}".format(spelling),
      headers={
        "X-Mashape-Key": "11SWTKGpRomshXZD5oHV4RUH1XAIp1SLSckjsnGDefU3k5Zfyd",
        "Accept": "application/json"
      }
    )
    response_json = json.loads(response.text)
    suggestion = response_json.get("suggestion")
    if str(suggestion).lower() == spelling:
        #print("Identical \n{}\n{}".format(spelling, suggestion))
        return("Looks good to me.")
    else:
        #print("{}\n{}".format(spelling, suggestion))
        return("{}*".format(suggestion))

#check_spelling("this setence has problems")