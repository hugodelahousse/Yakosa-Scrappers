import json
import logging

import yaml
from requests.exceptions import RequestException
from contextlib import closing
import unidecode as unidecode
import requests


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


def brand_by_name_get(url):
    try:
        with closing(requests.get(url)) as resp:
            if resp.status_code == 200:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("brand_by_name_get")
        return None


def product_by_name_get(url):
    try:
        with closing(requests.get(url)) as resp:
            if resp.status_code == 200:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("product_by_name_get")
        return None


def promotion_post(url, promotion):
    try:
        with closing(requests.post(url, json=promotion.__dict__)) as resp:
            if resp.status_code == 201:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("product_by_name_get")
        return None


def position_get(url, address, postal_code):
    try:
        with closing(requests.get(url, params={'q': address, 'postcode': postal_code})) as resp:
            if resp.status_code == 200:
                return json.loads(resp.content)
            else:
                return None
    except RequestException as e:
        logging.exception("position_get")
        return None


brands = {
    'Atac': 1,
    'Auchan Drive': 2,
    'Carrefour Contact': 3,
    'Carrefour Express': 4,
    'Carrefour Market': 5,
    'Carrefour': 6,
    'Casino Drive': 7,
    'Casino Shop': 8,
    'Colruyt': 9,
    'Cora': 10,
    'Franprix': 11,
    'Geant Casino': 12,
    'Geant': 13,
    'Intermarche': 14,
    'Leader Price': 15,
    'Leclerc Drive': 16,
    'Leclerc': 17,
    'Lidl': 18,
    'Magasin U': 19,
    'Monoprix': 20,
    'Petit Casino': 21,
    'Sherpa': 22,
    'Simply Market': 23,
    'Spar': 24,
    'Vival': 25,
    'Marche U': 26,
    'U Express': 27,
    'Super U': 28,
    'Aldi': 29,
    'Match': 30,
    'Netto': 31,
    'Auchan': 32,
    'Auchan Supermarche': 33,
    'Hyper U': 34,
    'Casino': 35,
}


def raw_brand_to_brand(raw_brand):
    for brand, value in brands.items():
        if brand.lower() in unidecode.unidecode(raw_brand.lower()):
            return f"@brand{value}"
    raise ValueError(f'Any brand is matching {raw_brand}')


def raw_brand_to_formated_brand(raw_brand):
    for brand, value in brands.items():
        if brand.lower() in unidecode.unidecode(raw_brand.lower()):
            return brand
    raise ValueError(f'Any brand is matching {raw_brand}')


def export(data, path):
    with open(path, 'w') as file:
        yaml.dump(data, file)
