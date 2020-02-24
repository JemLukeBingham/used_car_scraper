import scrapy
from urllib.parse import urljoin
from text_formatting import format_mileage, format_year, format_price

class GumtreeSpider(scrapy.Spider):
    name = 'gumtree'
    base_url = 'https://www.gumtree.co.za/'
    start_urls = [
        urljoin(base_url, 's-cars-bakkies/v1c9077p1'),
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
        next_page = response.xpath("//div[@class='pagination-content']/span/a[@class=' icon-pagination-right']/@href").get() 
        if next_page is not None:
            yield response.follow(urljoin(self.base_url, next_page), self.parse)
