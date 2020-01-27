import scrapy

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
            yield car
        next_page = response.xpath("//nav/ul/li/a[@aria-label='Next']/@href").get() 
        if next_page is not None:
            yield response.follow(next_page, self.parse)
