import unidecode as unidecode
from bs4 import BeautifulSoup
from datetime import timedelta
from src.scripts.utils import simple_get
from src.scripts.scraper import Scrapper
from src.models.Store import Store

brands = {
    'Atac',
    'Auchan Drive',
    'Carrefour Contact',
    'Carrefour Express',
    'Carrefour Market',
    'Carrefour',
    'Casino Drive',
    'Casino Drive',
    'Casino Shop',
    'Colruyt',
    'Cora',
    'Franprix',
    'Geant Casino',
    'Geant',
    'Intermarche',
    'Leader Price',
    'Leclerc Drive',
    'Leclerc',
    'Lidl',
    'Magasin U',
    'Monoprix',
    'Petit Casino',
    'Petit Casinon',
    'Sherpa',
    'Simply Market',
    'Spar',
    'Vival',
}


def raw_brand_to_brand(raw_brand):
    for brand in brands:
        if brand.lower() in unidecode.unidecode(raw_brand.lower()):
            return brand
    raise ValueError(f'Any brand is matching {raw_brand}')


def store_div_to_store(store_div):
    brand = store_div.find('b').contents[0]
    location = store_div.find_all('br')
    address = str(location[2].next)
    postal_code = str(location[3].next).split()[0]
    return Store(raw_brand_to_brand(brand), address, postal_code)


def get_departments(url):
    page = BeautifulSoup(simple_get(url), 'html.parser')
    columns = page.find_all('table')[2] \
        .find('tr') \
        .find_all('td')
    departments = []
    for column in columns:
        for row in column.find_all('a'):
            departments.append(row['href'])
    return departments


def get_cities(url):
    page = BeautifulSoup(simple_get(url), 'html.parser')
    columns = page.find_all('table')[4] \
        .find('tr') \
        .find_all('td')[2]
    cities = []
    for column in columns:
        for row in column.find_all('a'):
            cities.append(row['href'])
    return cities


def get_stores(url):
    page = BeautifulSoup(simple_get(url), 'html.parser')
    return page.find_all('table')[4] \
        .find('tr') \
        .find_all('td')[3] \
        .find_all('div')


class StoreScraper(Scrapper):
    time = timedelta(days=1)
    url = "https://supermarches.grandes-enseignes.com"

    def fetch(self, url):
        '''
        departments = get_departments(self.url)
        cities = []
        for department in departments:
            cities.extend(get_cities(f'{self.url}{department}'))
        stores = []
        for city in cities:
            stores.extend(get_cities(city))
        '''
        return get_stores("https://supermarches.grandes-enseignes.com/01-ain/01003-amareins.php")

    def transform(self, soup):
        stores = []
        for store_div in soup:
            stores.append(store_div_to_store(store_div))
        return stores

    def frequency(self, time):
        self.time = time

    def run(self):
        soup = self.fetch(None)
        stores = self.transform(soup)
        tmp = 2
        '''
        promotions = self.transform(soup)
        for promotion in promotions:
            promotion_post(API_URL + 'promotions', promotion)
        '''


if __name__ == "__main__":
    scraper = StoreScraper()
    soup = scraper.fetch(None)
    stores = scraper.transform(soup)
    tmp = 2
