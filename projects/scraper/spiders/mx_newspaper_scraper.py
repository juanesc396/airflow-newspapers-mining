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
country = 'Mexico'
language = 'Spanish'

months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
          'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


class ElUniversalSpider(scrapy.Spider):
    name = 'ElUniversalSpider'
    start_urls = ['https://www.eluniversal.com.mx/']
    allowed_domains = ['eluniversal.com.mx']

    def parse(self, response):
        news_links = response.xpath('//h3/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.eluniversal.com.mx'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath('//h2[@class="h2"]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Universal',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class DiariodeMexicoSpider(scrapy.Spider):
    name = 'DiariodeMexicoSpider'
    start_urls = ['https://www.diariodemexico.com/']
    allowed_domains = ['diariodemexico.com']

    def parse(self, response):
        news_links = response.xpath(
            '//h2/a/@href | //article/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.diariodemexico.com' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath('//h2[@class="lead"]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Diario de Mexico',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class ElSoldeMexicoSpider(scrapy.Spider):
    name = 'ElSoldeMexicoSpider'
    start_urls = ['https://www.elsoldemexico.com.mx/']
    allowed_domains = ['elsoldemexico.com.mx']

    def parse(self, response):
        news_links = response.xpath('//h4//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.elsoldemexico.com.mx' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath('//h3[@class="subtitle"]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Sol de Mexico',
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
    start_urls = ['https://www.razon.com.mx/']
    allowed_domains = ['razon.com.mx']

    def parse(self, response):
        news_links = response.xpath('//h2/a/@href | //h1//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.razon.com.mx' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath(
            '//h2[@class="article-epigraph  "]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'La Razon',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class MilenioSpider(scrapy.Spider):
    name = 'MilenioSpider'
    start_urls = ['https://www.milenio.com/']
    allowed_domains = ['milenio.com']

    def parse(self, response):
        news_links = response.xpath('//h2/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.milenio.com' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1/text()').get()
        epigraph = response.xpath(
            '//h2[@class="nd-title-headline-title-headline-base__abstract"]//text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'Milenio',
            'language': language,
            'country': country,
            'link': response.url,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


def run_mx_spiders():
    configure_logging()
    runner = CrawlerRunner()

    runner.crawl(ElUniversalSpider)
    runner.crawl(DiariodeMexicoSpider)
    runner.crawl(ElSoldeMexicoSpider)
    runner.crawl(LaRazonSpider)
    runner.crawl(MilenioSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


run_mx_spiders()
