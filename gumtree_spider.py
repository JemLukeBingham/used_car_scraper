import scrapy
import logging

def format_mileage(mileage):
    """
    Formats mileage text data from automart. Returns int in kilometres.
    """
    try:
        return int(mileage.replace(" ", "").replace("km",""))
    except (ValueError, TypeError):
        logging.warning("Could not convert mileage data to int: %s" % mileage)
        return mileage

def format_year(year):
    """
    Formats year text data from automart. Returns int.
    """
    try:
        return int(year)
    except (ValueError, TypeError):
        logging.warning("Could not convert year data to int: %r" % year)
        return year

def format_price(price):
    if price is None:
        return price
    try:
        return float(price.replace(" ", "").replace(",","").replace("R",""))
    except (ValueError, TypeError):
        logging.warning("Could not convert price data to float: %s" % price)
        return price

class CarSpider(scrapy.Spider):
    name = 'cars'
    start_urls = [
        'https://www.gumtree.co.za/s-cars-bakkies/v1c9077p1',
    ]
    def parse(self, response):
        for result in response.xpath("//div[@class='view']/div[@id='srpAds']/div[@class='related-items']/div[@class='related-content']/div/div[@class='related-ad-content']"):
            car = {}
            price = result.xpath("div[@class='price']/span/span[@class='ad-price']/text()").get()
            car['price'] = format_price(price)
            car['description'] = result.xpath("div[@class='description-content']/span[@class='related-ad-description']/span[@class='description-text']/text()").get()
            yield car
        #next_page = response.xpath("//nav/ul/li/a[@aria-label='Next']/@href").get() 
        #if next_page is not None:
        #    yield response.follow(next_page, self.parse)
