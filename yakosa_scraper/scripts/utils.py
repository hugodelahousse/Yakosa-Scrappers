import os
import json
import logging

import yaml
from requests.exceptions import RequestException
from contextlib import closing
import requests

JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZSwidXNlcklkIjpudWxsfQ.WVD-oHmdYbMNPAcdyzBh07S8ZXyyXblAtrkCRKuvkfo"


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def simple_get(url):
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        logging.exception("simple_get")
        return None


def position_get(url, address, postal_code):
    try:
        with closing(requests.get(url, params={'q': address, 'postcode': postal_code},
                                  headers={'Authorization': f"access_token {JWT_TOKEN}"})) as resp:
            if resp.status_code == 200:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("position_get")
        return None


def promotion_get(url):
    try:
        with closing(requests.get(url, headers={'Authorization': f"access_token {JWT_TOKEN}"})) as resp:
            if resp.status_code == 200:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("position_get")
        return None


def promotion_post(url, promotion):
    try:
        with closing(requests.post(url, json=promotion.__dict__,
                                   headers={'Authorization': f"access_token {JWT_TOKEN}"})) as resp:
            if resp.status_code == 201:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("product_post")
        return None


def brand_post(url, brand):
    try:
        with closing(requests.post(url, json=brand.__dict__,
                                   headers={'Authorization': f"access_token {JWT_TOKEN}"})) as resp:
            if resp.status_code == 201:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("promotion_post")
        return None


def store_post(url, store):
    try:
        with closing(requests.post(url, json=store.__dict__,
                                   headers={'Authorization': f"access_token {JWT_TOKEN}"})) as resp:
            if resp.status_code == 201:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("store_post")
        return None


def promotion_delete(url):
    try:
        with closing(requests.delete(url, params={'id': id}, headers={'Authorization': f"access_token {JWT_TOKEN}"})) \
                as resp:
            if resp.status_code == 200:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("promotion_delete")
        return None


def export(data, path):
    with open(path, 'w') as file:
        yaml.dump(data, file)

