class Store:
    def __init__(self, brand_id, address, postal_code):
        self.brandId = brand_id
        self.address = address
        self.postal_code = postal_code


class MetaStore:
    def __init__(self, brand_id, position):
        self.brandId = brand_id
        geometry = position["geometry"]
        self.position = {"coordinates": geometry["coordinates"], "type": geometry["type"]}

