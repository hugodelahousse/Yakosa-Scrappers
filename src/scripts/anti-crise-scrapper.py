import datetime
from bs4 import BeautifulSoup
from datetime import timedelta
from src.models.Promotion import Promotion
from src.scripts.utils import simple_get, promotion_post
from src.scripts.scrapper import Scrapper
from src.scripts.config import API_URL, HISTORY_FILE


class AntiCriseScrapper(Scrapper):
    time = timedelta(days=1)
    url = "http://anti-crise.fr/les-catalogues-avec-optimisations/"

    @staticmethod
    def __get_history():
        values = []
        with open(HISTORY_FILE, "r") as file:
            for line in file:
                values.append(line[:len(line) - 1])
        return values

    @staticmethod
    def __extract_information(page, store_name, begin_date, end_date):
        cases = page.find("div", {"id": "price-table"}) \
            .find("div", {"id": "price-table-table"}) \
            .find("table") \
            .find_all("th")

        position = {'PRODUIT': None, 'Q': None, 'PRIX': None, 'PROMO': None}

        for i in range(len(cases)):
            if 'PRODUIT' in cases[i].string:
                position['PRODUIT'] = i
            elif 'Q' in cases[i].string:
                position['Q'] = i
            elif 'PRIX' in cases[i].string:
                position['PRIX'] = i
            elif 'PROMO' in cases[i].string:
                position['PROMO'] = i

        promotion_array = page.find("div", {"id": "price-table"}) \
            .find("div", {"id": "price-table-table"}) \
            .find("table") \
            .find_all("tr")
        promotion_array = promotion_array[1:]

        scraped_promotions = []

        for promotion_data in promotion_array:
            cell = promotion_data.find_all("td")
            product_name = cell[position['PRODUIT']].string
            product_price = cell[position['PRIX']].string.replace("€", "")
            product_promo = cell[position['PROMO']].string.replace("€", "")
            product_quantity = cell[position['Q']].string
            promotion = Promotion(store_name, begin_date, end_date, product_name, product_price, product_promo,
                                  product_quantity)
            scraped_promotions.append(promotion)

        return scraped_promotions

    def fetch(self, url):
        page = BeautifulSoup(simple_get(self.url), 'html.parser')
        history = self.__get_history()

        brand_names = []
        for brand_name in page.find_all("h2")[1:]:
            brand_names.append(brand_name.text.strip())

        newspapers_brand = []

        stores = page.find_all("div", {"class": "block-items-catalogue"})
        with open(HISTORY_FILE, "a") as file:
            for i in range(len(stores)):
                newspapers = stores[i].find_all("div")

                for newspaper in newspapers:
                    dates = newspaper.find("h6").text.split("-")
                    begin_date = datetime.datetime.strptime(dates[0].strip(), '%d/%m/%Y').isoformat()
                    end_date = datetime.datetime.strptime(dates[1].strip(), '%d/%m/%Y').isoformat()
                    information = {'brand': brand_names[i], 'begin_date': begin_date, 'end_date': end_date}
                    id = f"{information['brand']}-{information['begin_date']}-{information['end_date']}"
                    if id not in history:
                        file.write(id + '\n')
                        information['url'] = newspaper.find("a", {"class": "info"})['href']
                        newspapers_brand.append(information)

        return newspapers_brand

    def transform(self, soup):
        products = []

        for element in soup:
            page = BeautifulSoup(simple_get(element['url']), 'html.parser')
            promotions = self.__extract_information(page, element['brand'], element['begin_date'], element['end_date'])
            for scraped_promotion in promotions:
                converted = scraped_promotion.convertToPromotion(API_URL)
                if converted is not None:
                    products.append(converted)

        tmp = list(dict.fromkeys(products))
        return tmp

    def frequency(self, time):
        self.time = time

    def run(self):
        soup = self.fetch(None)
        promotions = self.transform(soup)
        for promotion in promotions:
            promotion_post(API_URL + 'promotions', promotion)
