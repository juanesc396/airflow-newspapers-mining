import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import pymongo

import os
from datetime import datetime

# Getting the IP of the PC
IP_LOCAL = os.environ.get('IPPC')

myclient = pymongo.MongoClient(f"mongodb://{IP_LOCAL}:27017/")
my_db = myclient['Newspapers']
today = datetime.today().strftime('%Y-%m-%d')
country = 'Spain'
language = 'Spanish'

months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
          'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


class ElMundoSpider(scrapy.Spider):
    name = 'ElMundoSpider'
    start_urls = ['https://www.elmundo.es/']
    allowed_domains = ['elmundo.es']

    def parse(self, response):
        news_links = response.xpath('//header/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.elmundo.es'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1[@class="headline-text"]/text()').get()
        epigraph = response.xpath(
            '//p[@class="ue-c-article__standfirst"]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'ElMundo',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class EldiarioSpider(scrapy.Spider):
    name = 'EldiarioSpider'
    start_urls = ['https://www.eldiario.es/']
    allowed_domains = ['eldiario.es']

    def parse(self, response):
        news_links = response.xpath('//h2/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.eldiario.es'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath('//h2/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Diario',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class ElEspañolSpider(scrapy.Spider):
    name = 'ElEspañolSpider'
    start_urls = ['https://www.elespanol.com/']
    allowed_domains = ['elespanol.com']

    def parse(self, response):
        news_links = response.xpath('//h2/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.elespanol.com'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath('//h2/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Español',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class LaRazonSpider(scrapy.Spider):
    name = 'LaRazonSpider'
    start_urls = ['https://www.larazon.es/']
    allowed_domains = ['larazon.es']

    def parse(self, response):
        news_links = response.xpath('//h3/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.larazon.es'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath('//h2/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'La Razon España',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class ABCSpider(scrapy.Spider):
    name = 'ABCSpider'
    start_urls = ['https://www.abc.es/']
    allowed_domains = ['abc.es']

    def parse(self, response):
        news_links = response.xpath('//h3/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                pass
            else:
                url = 'https://www.abc.es/'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath('//h2/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'ABC',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


def run_es_spiders():
    configure_logging()
    runner = CrawlerRunner()

    runner.crawl(ElMundoSpider)
    runner.crawl(EldiarioSpider)
    runner.crawl(ElEspañolSpider)
    runner.crawl(LaRazonSpider)
    runner.crawl(ABCSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


run_es_spiders()
