import requests
import json

def quote_of_the_day():
    try:
        url = 'https://quotes.rest/qod/'
        response = requests.get(url)
        response_json = json.loads(response.text)
        quote = response_json.get('quote')
        quote_author = response_json.get('author')

        quote_of_day = quote + ' - ' + quote_author

        return quote_of_day

    except Exception as e:
        # TODO: Handle correct exceptions properly
        print(e)
        return "Error Beep Boop"