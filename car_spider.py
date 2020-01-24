import scrapy

class CarSpider(scrapy.Spider):
    name = 'cars'
    start_urls = [
        'https://www.automart.co.za/used-cars/',
    ]

    def parse(self, response):
        for car in response.xpath("//div[@class='search-results']"):
            car_data = car.xpath('div/div/p/em/text()').getall()
            # require data has exact form [make, model]
            if len(car_data) == 2:
                yield {
                    'make': car_data[0],
                    'model': car_data[1]
                }
        next_page = response.xpath("//nav/ul/li/a[@aria-label='Next']/@href").get() 
        if next_page is not None:
            yield response.follow(next_page, self.parse)
