import scrapy
from ..items import Choicepet1Item

class Cpetscrape1Spider(scrapy.Spider):
    name = 'cpetscrape1'
    # allowed_domains = ['choicepet.com']
    # start_urls = ['http://choicepet.com/']
    

    def start_requests(self):
        url = r'https://choicepet.com/pages/locations-1'
        yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        items = Choicepet1Item()
        def coordinates(href):
            start = href[0].find('/@')
            end = href[0].find(',1')
            b = href[0][start+2:end]
            b = b.split(',')
            return b
        html_response = response.xpath('//div[@class="col-md-6"]')
        for i in html_response:
            list1 = i.xpath('div[contains(@class,"col-")]/p/strong/text()').extract()

            if len(list1)==0:
                continue

            timing = i.xpath('div[contains(@class,"col-")]/ul/li/text()').extract()
            loc = i.xpath('div[contains(@class,"col-")]/p/text()').extract()
            strstpin = []
            city = ''
            loc = ', '.join(loc)
            loc = loc.replace(', USA','')
            loc1 = loc.split(', ')

            for j in loc1:
                if j.replace(' ','').isalpha()==False:
                    strstpin.append(j)
                else:
                    city = j
            
            href = i.xpath('div[contains(@class,"col-")]/a[@rel="noopener noreferrer"]/@href').extract()
            cord = coordinates(href)

            items = {
                'StoreName': 'Choice Pet ' + list1[0], 
                'Street': strstpin[0], 
                'City': city, 
                'State': strstpin[1].split(' ')[0], 
                'StoreTiminings': ', '.join(timing),
                'Phone': ','.join(list1[2:]),
                'Latitude': cord[0],
                'Longitude': cord[1],
                'Zipcode' : strstpin[1].split(' ')[1],  
                }
            yield items
        


#$x('//div[@class="row loc-pg-row"]')
#$x('//div[@class="col-md-6"]//ul/li/text()')
#$x('//div[@class="col-md-6"]//p/text()')
# $x('//div[@class="col-md-6"]//a[@rel="noopener noreferrer"]/@href')
# $x('//div[@class="col-md-6"]//p/strong/text()')
