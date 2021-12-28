import scrapy

to_remove = '{}[]«#$%^&*._,1234567890+=<>/\()":;!?'
class project1(scrapy.Spider):
    # Name of the spider
    name = 'project1'
    # The domain to be scraped
    allowed_domains = ['www.ntb.kr']
    # The URLs from domain to scrape
    start_urls = ["https://www.ntb.kr/market/selectFullTechList.do"]

    # Spider default callback function
    def parse(self, response):
        title = response.xpath('//*[@id="imgList_1"]').getall()
        title="".join(c for c in title if c not in to_remove)

        # Yield all elements
        yield {"Title ": title}

        # title = response.xpath('//*[@id="imgList_1"]').getall()
        # for l in lists:

