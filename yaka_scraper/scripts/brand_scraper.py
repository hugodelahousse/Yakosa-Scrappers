import yaml
from datetime import timedelta

from config import API_URL
from scraper import Scrapper
from utils import brand_post

from models.utils import brands
from models.brand import MetaBrand


class StoreScraper(Scrapper):
    time = timedelta(days=1)

    def fetch(self, url):
        print('FETCH')
        pass

    def transform(self, soup):
        print('TRANSFORM')
        meta_brands = []
        for key, value in brands.items():
            meta_brands.append(MetaBrand(key))
        return meta_brands

    def frequency(self, time):
        self.time = time

    def run(self):
        for brand in self.transform(None):
            brand_post(API_URL + 'brands', brand)

    def export(self, data, path):
        with open(path, 'w') as file:
            final_data = dict()
            for i in range(len(data)):
                final_data[f'brand{i + 1}'] = data[i].__dict__
            yaml.dump({'items': final_data}, file)


if __name__ == "__main__":
    print('START')
    scraper = StoreScraper()
    scraper.run()
    print('FINISH')
