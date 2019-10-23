import yaml
import sentry_sdk
import unidecode as unidecode

from bs4 import BeautifulSoup
from datetime import timedelta

from config import API_URL
from utils import simple_get, position_get, store_post
from scraper import Scrapper

from models.store import Store, MetaStore
from models.utils import raw_brand_to_formated_brand, brands


def store_div_to_store(store_div):
    try:
        brand = store_div.find('b').contents[0]
        location = store_div.find_all('br')
        address = unidecode.unidecode(str(location[2].next))
        postal_code = str(location[3].next).split()[0]
        formated_brand = raw_brand_to_formated_brand(brand)
        return Store(brands[formated_brand], address, postal_code, str(brand))
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
        # 'https://supermarches.grandes-enseignes.com/91-essonne/91648-vert-le-grand.php' is the cities' array
        cities = ['https://supermarches.grandes-enseignes.com/94-val-de-marne/94043-le-kremlin-bicetre.php']
        '''
        for department in get_departments(self.url):
            for city in get_cities(f'{self.url}{department}'):
                cities.add(f'{self.url}{city}')
        '''
        stores = []
        for city in cities:
            stores.extend(get_stores(city))
        return stores

    def transform(self, soup):
        print('TRANSFORM')
        stores = set()
        for store_div in soup:
            store = store_div_to_store(store_div)
            if store:
                stores.add(store)
        meta_stores = []
        for store in stores:
            custom_address = store.address.replace(' ', '+')
            geo = position_get('https://api-adresse.data.gouv.fr/search/', custom_address, store.postal_code)
            if geo and len(geo["features"]):
                meta_stores.append(MetaStore(store.brandId, geo["features"][0], store.address, store.name))
        return meta_stores

    def frequency(self, time):
        self.time = time

    def run(self):
        soup = self.fetch(None)
        for store in self.transform(soup):
            store_post(API_URL + 'stores', store)

    def export(self, data, path):
        with open(path, 'w') as file:
            final_data = dict()
            for i in range(len(data)):
                data[i].brand = f'@brand{data[i].brandId}'
                del data[i].brandId
                final_data[f'store{i + 1}'] = data[i].__dict__
            yaml.dump({'items': final_data}, file)


if __name__ == "__main__":
    sentry_sdk.init("https://97da0dc50f574bf89ef1ee9f668f16ed@sentry.io/1794021")
    print('START')
    scraper = StoreScraper()
    scraper.run()
    print('FINISH')

