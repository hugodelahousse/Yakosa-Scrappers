import yaml

import unidecode as unidecode
from bs4 import BeautifulSoup
from datetime import timedelta

from src.scripts.config import META_STORE_FILE_YML
from src.scripts.utils import simple_get, position_get
from src.scripts.scraper import Scrapper
from src.models.Store import Store, MetaStore

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
}


def raw_brand_to_brand(raw_brand):
    for brand, value in brands.items():
        if brand.lower() in unidecode.unidecode(raw_brand.lower()):
            return f"@brand{value}"
    raise ValueError(f'Any brand is matching {raw_brand}')


def store_div_to_store(store_div):
    try:
        brand = store_div.find('b').contents[0]
        location = store_div.find_all('br')
        address = unidecode.unidecode(str(location[2].next))
        postal_code = str(location[3].next).split()[0]
        return Store(raw_brand_to_brand(brand), address, postal_code)
    except:
        return None


def get_departments(url):
    print(f'get_department : {url}')
    try:
        page = BeautifulSoup(simple_get(url), 'html.parser')
        columns = page.find_all('table')[2] \
            .find('tr') \
            .find_all('td')
        departments = []
        for column in columns:
            for row in column.find_all('a'):
                departments.append(row['href'])
        return departments
    except:
        print(f'ERROR get_departements : {url}')
        return []


def get_cities(url):
    print(f'get_cities : {url}')
    try:
        page = BeautifulSoup(simple_get(url), 'html.parser')
        columns = page.find_all('table')[4] \
            .find('tr') \
            .find_all('td')
        cities = []
        for column in columns:
            for row in column.find_all('a'):
                cities.append(row['href'])
        return cities
    except:
        print(f'ERROR get_cities : {url}')
        return []


def get_stores(url):
    print(f'get_store : {url}')
    try:
        page = BeautifulSoup(simple_get(url), 'html.parser')
        return page.find_all('table')[4] \
            .find('tr') \
            .find_all('td')[3] \
            .find_all('div')
    except:
        print(f'ERROR get_store : {url}')
        return []


class StoreScraper(Scrapper):
    time = timedelta(days=1)
    url = "https://supermarches.grandes-enseignes.com"

    def fetch(self, url):
        print('FETCH')
        # In order to scrapp only paris put this :
        # 'https://supermarches.grandes-enseignes.com/75-ville-de-paris/75100-paris.php' is the cities' array
        cities = []
        for department in get_departments(self.url):
            for city in get_cities(f'{self.url}{department}'):
                cities.append(f'{self.url}{city}')
        stores = []
        for city in cities:
            stores.extend(get_stores(city))
        return stores

    def transform(self, soup):
        print('TRANSFORM')
        stores = []
        for store_div in soup:
            store = store_div_to_store(store_div)
            if store:
                stores.append(store)
        stores = list(dict.fromkeys(stores))
        meta_stores = []
        for store in stores:
            print(store)
            address = store.address.replace(' ', '+')
            geo = position_get('https://api-adresse.data.gouv.fr/search/', address, store.postal_code)
            if geo and len(geo["features"]):
                meta_stores.append(MetaStore(store.brand, geo["features"][0]))
        return meta_stores

    def frequency(self, time):
        self.time = time

    def run(self):
        soup = self.fetch(None)
        stores = self.transform(soup)
        with open(META_STORE_FILE_YML, 'w') as file:
            final_stores = dict()
            for i in range(len(stores)):
                final_stores[f'store{i + 1}'] = stores[i].__dict__
            yaml.dump({'items': final_stores}, file)


if __name__ == "__main__":
    print('START')
    scraper = StoreScraper()
    scraper.run()
    print('FINISH')
