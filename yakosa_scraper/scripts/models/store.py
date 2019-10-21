class Store:
    def __init__(self, brand_id, address, postal_code, name):
        self.brandId = brand_id
        self.address = address
        self.postal_code = postal_code
        self.name = name


class MetaStore:
    def __init__(self, brand_id, position, address, name):
        self.brandId = brand_id
        geometry = position["geometry"]
        self.position = {"coordinates": geometry["coordinates"], "type": geometry["type"]}
        self.address = address
        self.name = name

