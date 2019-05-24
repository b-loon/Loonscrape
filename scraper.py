#! /usr/bin/env python3

from functools import partial
import configparser
import json
import requests

config = configparser.ConfigParser()
config.read('config.ini')
API_KEY = config.get('scraper', 'api_key')
API_URL = config.get('scraper', 'base_url') + config.get('scraper', 'api_url_extension')
BASE_URL = config.get('scraper', 'base_url')
CALLSIGN = config.get('balloon', 'callsign')

VALID_WHAT_REQUESTS = {'loc', 'wx', 'msg'}


def get_aprs_data(what):
    if what not in VALID_WHAT_REQUESTS:
        error_message = f"{what!r} is not in the list of permissible what requests: {list(VALID_WHAT_REQUESTS)}"
        raise Exception(error_message)

    query_params = {
        'apikey': API_KEY,
        'format': 'json',
        'name': CALLSIGN,
        'what': what,
    }

    if 'msg' == what:
        query_params['dst'] = CALLSIGN

    response_object = requests.get(API_URL, params=query_params)
    response_object.raise_for_status()
    response = response_object.json()

    print(json.dumps(response, indent=4))

    return response


get_location_data = partial(get_aprs_data, what='loc')
get_weather_data = partial(get_aprs_data, what='wx')
get_latest_message_data = partial(get_aprs_data, what='msg')

if __name__ == '__main__':
    # EXAMPLE USAGE
    location_data = get_location_data()
    print(json.dumps(location_data, indent=4))
