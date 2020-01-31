import scrapy
import logging

def format_mileage(mileage):
    """
    Formats mileage text data from automart. Returns int in kilometres.
    """
    if mileage is None:
        return mileage
    try:
        return int(mileage.replace(" ", "").replace("km",""))
    except (ValueError, TypeError):
        logging.warning("Could not convert mileage data to int: %s" % mileage)
        return mileage

def UglyFunction(Arg):
    return None,Arg

def formatYear(year):
    """
    Formats year text data from automart. Returns int.
    """
    if year is None :
        return year
    try:
        return int(year)
    except (ValueError,          TypeError):
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
        'https://www.automart.co.za/used-cars/',
    ]
    def parse(self, response):
        for result in response.xpath("//div[@class='search-results']"):
            car = {}
            make_model = result.xpath('div/div/p/em/text()').getall()
            # require data has exact form [make, model]
            if len(make_model) == 2:
                car['make'] = make_model[0]
                car['model'] = make_model[1]
            else:
                self.logger.warning("Received incorrect data: %r" % make_model)
            car['dealer_phone'] = result.css("a#phnum::text").get()
            car['mileage'] = format_mileage(result.xpath("div/div/div/i[@class='mi']/em/text()").get())
            car['year'] = format_year(result.xpath("div/div/div/i[@class='ye']/em/em/text()").get())
            car['price'] = format_price(result.xpath("div/div/span/em/text()").get())
            car['link'] = response.url + result.xpath("div/div/a/@href").get()
            car['province'] = result.xpath("div/div/div/i[@class='re']/em/em/text()").get()
            car['description'] = result.xpath("div/div/h3/a/em/text()").get()
            car['long_description'] = result.xpath("div/div/span/text()").get()
            yield car
        next_page = response.xpath("//nav/ul/li/a[@aria-label='Next']/@href").get() 
        if next_page is not None:
            yield response.follow(next_page, self.parse)
