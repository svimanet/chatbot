import requests
import json
import os


def get_station_status(station_name):
    station_list = "{}/stations.json".format(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isfile(station_list):
        url = "http://gbfs.urbansharing.com/bergen-city-bike/station_information.json"
        response = requests.get(url)
        assert response.status_code == 200
        raw_json = json.loads(response.text)
        with open(station_list, "w+") as data_file:
            json.dump(raw_json, data_file)
        get_station_status(station_name)

    else:
        stations = json.load(open(station_list))
        for station in stations["data"]["stations"]:
            #print("\n# {} - {}".format(station_name.strip(), str(station["name"]).lower().strip()))
            if station_name.lower().strip() in station["name"].lower().strip():
                return get_status(station["name"], station["station_id"], station["capacity"])
        return "Couldn't find {}".format(station_name)


def get_status(name, station_id, cap):
    url = "http://gbfs.urbansharing.com/bergen-city-bike/station_status.json"
    response = requests.get(url)
    assert response.status_code == 200
    status = json.loads(response.text)
    #print("{}, {}".format(station_id, name))
    for station in status["data"]["stations"]:
        if station["station_id"] == station_id:
            data = "{} - {}/{} available bikes.".format(name.strip(), station["num_bikes_available"], cap).title()
            return data
    return "¯\\_(ツ)_/¯"