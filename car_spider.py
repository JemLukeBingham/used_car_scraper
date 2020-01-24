import scrapy

class CarSpider(scrapy.Spider):
    name = 'cars'
    start_urls = [
        'https://www.automart.co.za/used-cars/',
    ]

    def parse(self, response):
        for car in response.xpath("//div[@class='search-results']"):
            make, model = car.xpath('div/div/p/em/text()').getall()
            yield {
                'make': make,
                'model': model 
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
