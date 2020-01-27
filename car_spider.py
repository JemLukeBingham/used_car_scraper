import scrapy
import logging

def format_mileage(text):
    """
    Formats mileage text data from automart. Returns int in kilometres.
    """
    try:
        return int(text.replace(" ", "").replace("km",""))
    except ValueError:
        logging.warning("Could not convert data to int: %s" % text)
        return None

def format_year(text):
    """
    Formats year text data from automart. Returns int.
    """
    return int(text)

def format_price(text):
    try:
        return float(text.replace(" ", "").replace(",","").replace("R",""))
    except ValueError:
        logging.warning("Could not convert price data to float: %s" % text)
        return None

class CarSpider(scrapy.Spider):
    name = 'cars'
    start_urls = [
        'https://www.automart.co.za/used-cars/',
    ]
    def parse(self, response):
        for result in response.xpath("//div[@class='search-results']"):
            car = {}
            make_model = result.xpath('div/div/p/em/text()').getall()
            # require data has exact form [make, model]
            if len(make_model) == 2:
                car['make'] = make_model[0],
                car['model'] = make_model[1],
            else:
                self.logger.warning("Received incorrect data: %r" % make_model)
            car['dealer_phone'] = result.css("a#phnum::text").get()
            car['mileage'] = format_mileage(result.xpath("div/div/div/i[@class='mi']/em/text()").get())
            car['year'] = format_year(result.xpath("div/div/div/i[@class='ye']/em/em/text()").get())
            car['price'] = format_price(result.xpath("div/div/span/em/text()").get())
            yield car
        next_page = response.xpath("//nav/ul/li/a[@aria-label='Next']/@href").get() 
        if next_page is not None:
            yield response.follow(next_page, self.parse)
