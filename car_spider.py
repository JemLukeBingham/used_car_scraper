import scrapy

class CarSpider(scrapy.Spider):
    name = 'cars'
    start_urls = [
        'https://www.automart.co.za/used-cars/',
    ]

    def parse(self, response):
        for car in response.xpath("//div[@class='search-results']"):
            make_model = car.xpath('div/div/p/em/text()').getall()
            # require data has exact form [make, model]
            if len(make_model) == 2:
                yield {
                    'make': make_model[0],
                    'model': make_model[1],
                    'dealer_phone':car.css("a#phnum::text").get()
                }
            else:
                self.logger.warning("Received incorrect data: %r" % make_model)
        next_page = response.xpath("//nav/ul/li/a[@aria-label='Next']/@href").get() 
        #if next_page is not None:
        #    yield response.follow(next_page, self.parse)
