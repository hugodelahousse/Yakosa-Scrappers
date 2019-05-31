class Store:
    def __init__(self, brand, address, postal_code):
        self.brand = brand
        self.address = address
        self.postal_code = postal_code


class MetaStore:
    def __init__(self, brand, position):
        self.brand = brand
        geometry = position["geometry"]
        self.position = {"coordinates": geometry["coordinates"], "type": geometry["type"]}

