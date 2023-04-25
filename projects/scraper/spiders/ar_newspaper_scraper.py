import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import pymongo

import os
from datetime import datetime

# Getting the IP of the host
IP_LOCAL = os.environ.get('IPPC')

myclient = pymongo.MongoClient(f"mongodb://{IP_LOCAL}:27017/")
my_db = myclient['Newspapers']
today = datetime.today().strftime('%Y-%m-%d')
country = 'Argentina'
language = 'Spanish'

months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
          'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


class LitoralSpider(scrapy.Spider):
    name = 'LitoralSpider'
    start_urls = ['https://www.ellitoral.com/']
    allowed_domains = ['ellitoral.com']

    def parse(self, response):
        news_links = response.xpath(
            '//div[@class="flex-content _cdcy1 "]//div/div/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.ellitoral.com'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1[@class="headline-text"]/text()').get()
        epigraph = response.xpath('//h2/p/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Litoral',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class LaNacionSpider(scrapy.Spider):
    name = 'LaNacionSpider'
    start_urls = ['https://www.lanacion.com.ar/']
    allowed_domains = ['lanacion.com.ar']

    def parse(self, response):
        news_links = response.xpath('//h2/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.lanacion.com.ar'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath(
            '//h2[@class="com-subhead --bajada --m-xs"]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'La Nacion',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class ClarinSpider(scrapy.Spider):
    name = 'ClarinSpider'
    start_urls = ['https://www.clarin.com/']
    allowed_domains = ['clarin.com']

    def parse(self, response):
        news_links = response.xpath(
            '//li/@aria-label | //a[@class="link_article"]/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.clarin.com'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath('//h2/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'Clarin',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class Pagina12Spider(scrapy.Spider):
    name = 'Pagina12Spider'
    start_urls = ['https://www.pagina12.com.ar/']
    allowed_domains = ['pagina12.com.ar']

    def parse(self, response):
        news_links = response.xpath(
            '//div[@class="article-title "]//a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.pagina12.com.ar'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath('//div[@class="col 2-col"]/h3/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'Pagina 12',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class InfobaeSpider(scrapy.Spider):
    name = 'InfobaeSpider'
    start_urls = ['https://www.infobae.com/']
    allowed_domains = ['infobae.com']

    def parse(self, response):
        news_links = response.xpath('//a[@class="cst_ctn"]/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.infobae.com'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath(
            '//h2[@class="article-subheadline"]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'Infobae',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


def run_ar_spiders():
    configure_logging()
    runner = CrawlerRunner()

    runner.crawl(LitoralSpider)
    runner.crawl(LaNacionSpider)
    runner.crawl(ClarinSpider)
    runner.crawl(Pagina12Spider)
    runner.crawl(InfobaeSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


run_ar_spiders()
