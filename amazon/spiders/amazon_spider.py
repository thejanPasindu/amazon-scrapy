import scrapy
from amazon.items import AmazonItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    number = 3
    def start_requests(self):
        urls = [
            'https://www.amazon.com/s?i=specialty-aps&srs=17276793011&page=2&qid=1570782228&ref=lp_17276793011_pg_2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = AmazonItem()
        for data in response.css('.s-include-content-margin .sg-row , .a-color-base.a-text-normal'):
            # print(data)
            # yield data
            item['name'] = str(data.css('span.a-color-base.a-text-normal::text').get())
            item['author'] = str(data.css('.a-color-secondary .a-size-base.a-link-normal::text').get()).strip().split('\n')[0]
            item['price'] = str(data.css('.a-spacing-top-small .a-price-whole::text').get())
            if(item['name']!="None" and item['author']!="None" and item['price']!="None"):
                yield item
                print("---"*50)
            else:
                pass

        next_page = 'https://www.amazon.com/s?i=specialty-aps&srs=17276793011&page='+ str(QuotesSpider.number) +'&qid=1570782228&ref=lp_17276793011_pg_2'
        if(QuotesSpider.number<=10):
            QuotesSpider.number+=1
            yield response.follow(next_page, callback=self.parse)