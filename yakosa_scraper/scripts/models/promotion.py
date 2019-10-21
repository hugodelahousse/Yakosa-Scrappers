import unidecode as unidecode
from .utils import brand_by_name_get, product_by_name_get, raw_brand_to_formated_brand


class Promotion:
    def __init__(self, store_name, begin_date, end_date, name, price, promo, quantity):
        self.store_name = raw_brand_to_formated_brand(store_name)
        self.beginDate = begin_date
        self.endDate = end_date
        self.name = unidecode.unidecode(name)
        self.price = price
        self.promotion = promo
        self.quantity = int(quantity)

    def __str__(self):
        return f'Store: {self.store_name} / Product name: {self.name} / Product price: {self.price} / Promotion: {self.promotion}'

    def convertToPromotion(self, url):
        brand_id = brand_by_name_get(url + "brands/" + self.store_name)
        if brand_id is not None:
            brand_id = brand_id["id"]
        product = product_by_name_get(url + "products/name/" + self.name)
        if product is not None:
            product = product["barcode"]
        else:
            return None
        type = self.quantity - 1 if self.quantity < 3 else 3
        return MetaPromotion("", self.beginDate, self.endDate, None, None, brand_id, product, self.price,
                             self.promotion, type, self.quantity)


class MetaPromotion:
    def __init__(self, description, begin_date, end_date, user_id, store_id, brand_id, product, price, promotion, type,
                 quantity):
        self.description = description
        self.beginDate = begin_date
        self.endDate = end_date
        self.userId = user_id
        self.storeId = store_id
        self.brandId = brand_id
        self.product = product
        self.price = price
        self.promotion = promotion
        self.type = type
        self.unit = 0
        self.quantity = quantity
