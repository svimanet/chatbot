import requests
import json
import re

API_URL = 'https://api.covid19api.com/summary'

def get_covid_cases_by_country(country):
    try:
        response = requests.get(API_URL)
        response_json = json.loads(response.text)

        if response_json['Message'] == 'Caching in progress':
            return 'API Caching in progress, please try again later.'

        country_data = next((data for data in response_json['Countries'] if data['Country'].lower() == country.lower()), {})

        if country_data:
            covid_info = '\
                COVID-19 Cases for {Country} ({CountryCode}) - New Confirmed Cases: {NewConfirmed}, \
                    Total Confirmed Cases: {TotalConfirmed}, \
                        New Deaths: {NewDeaths}, \
                            Total Deaths: {TotalDeaths}, \
                                New Recovered Cases: {NewRecovered}, \
                                    Total Recovered Cases: {TotalRecovered}'
                

            return re.sub(r"\s\s+" , " ", covid_info.format(**country_data))

        else:
            return 'Invalid Country Name'

    except Exception as e:
        print(e)
        return 'Error Fetching COVID-19 Data'


def get_global_covid_cases():
    try:
        response = requests.get(API_URL)
        response_json = json.loads(response.text)

        if response_json['Message'] == 'Caching in progress':
            return 'API Caching in progress, please try again later.'

        global_data = response_json['Global']

        global_covid_info = '\
            Global COVID-19 Cases - New Confirmed Cases: {NewConfirmed}, \
                Total Confirmed Cases: {TotalConfirmed}, \
                    New Deaths: {NewDeaths}, \
                        Total Deaths: {TotalDeaths}, \
                            New Recovered Cases: {NewRecovered}, \
                                Total Recovered Cases: {TotalRecovered}'

        return re.sub(r"\s\s+" , " ", global_covid_info.format(**global_data))

    except Exception as e:
        print(e)
        return 'Error Fetching COVID-19 Data'