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
country = 'Chile'
language = 'Spanish'

months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
          'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


class LaTerceraSpider(scrapy.Spider):
    name = 'LaTerceraSpider'
    start_urls = ['https://www.latercera.com/']
    allowed_domains = ['latercera.com']

    def parse(self, response):
        news_links = response.xpath(
            '//h4//@href | //h3//@href | //h2//@href | //h1//@href | //h5//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.latercera.com'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath('//p[@class="excerpt"]//text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'La Tercera',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class EmolSpider(scrapy.Spider):
    name = 'EmolSpider'
    start_urls = ['https://www.emol.com/']
    allowed_domains = ['emol.com']

    def parse(self, response):
        news_links = response.xpath(
            '//div[@class="contenedor-titulo"]//@href | //h1//@href | //h2//@href | //h3//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.emol.com' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath(
            '//div[@class="cont_iz_titulobajada"]//h2//text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'Emol',
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
    start_urls = ['https://www.larazon.cl/']
    allowed_domains = ['larazon.cl']

    def parse(self, response):
        news_links = response.xpath('//h4//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.larazon.cl' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath(
            '//div[@class="article__announce-text"]//text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'La Razon Chile',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class ElNorteñoSpider(scrapy.Spider):
    name = 'ElNorteñoSpider'
    start_urls = ['https://www.elnortero.cl/']
    allowed_domains = ['elnortero.cl']

    def parse(self, response):
        news_links = response.xpath('//h4//@href | //h3//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.elnortero.cl' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath(
            '//div[@class="field-field-noticia-bajada"]//text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Norteño',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


class ElMostradorSpider(scrapy.Spider):
    name = 'ElMostradorSpider'
    start_urls = ['https://www.elmostrador.cl/']
    allowed_domains = ['elmostrador.cl']

    def parse(self, response):
        news_links = response.xpath('//h3//@href | //h4//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.elmostrador.cl' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath(
            '//section//h2[@class="titulo-single"]/text()').get()
        epigraph = response.xpath(
            '//article[@class="col-sm-12 col-md-12"]//figcaption/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Mostrador',
            'language': language,
            'country': country,
            'link': response.url
        }

        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)


def run_cl_spiders():
    configure_logging()
    runner = CrawlerRunner()

    runner.crawl(LaTerceraSpider)
    runner.crawl(EmolSpider)
    runner.crawl(LaRazonSpider)
    runner.crawl(ElNorteñoSpider)
    runner.crawl(ElMostradorSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


run_cl_spiders()
