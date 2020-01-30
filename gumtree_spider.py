import scrapy
from text_formatting import format_mileage, format_year, format_price

class GumtreeSpider(scrapy.Spider):
    name = 'gumtree'
    start_urls = [
        'https://www.gumtree.co.za/s-cars-bakkies/v1c9077p1',
    ]
    def parse(self, response):
        for result in response.xpath("//div[@class='view']/\
                                        div[@id='srpAds']/\
                                        div[@class='related-items']/\
                                        div[@class='related-content']/\
                                        div/div[@class='related-ad-content']"):
            car = {}
            price = result.xpath("div[@class='price']/span/span[@class='ad-price']/text()").get()
            car['price'] = format_price(price)
            car['description'] = result.xpath("div[@class='description-content']/\
                                               span[@class='related-ad-description']/\
                                               span[@class='description-text']/text()").get()
            yield car
        #next_page = response.xpath("//nav/ul/li/a[@aria-label='Next']/@href").get() 
        #if next_page is not None:
        #    yield response.follow(next_page, self.parse)
