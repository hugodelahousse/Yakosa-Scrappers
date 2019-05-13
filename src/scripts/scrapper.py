from abc import abstractmethod


class Scrapper:

    @abstractmethod
    def fetch(self, url):
        pass

    @abstractmethod
    def transform(self, soup):
        pass

    @abstractmethod
    def frequency(self, time):
        pass

    @abstractmethod
    def run(self):
        pass
