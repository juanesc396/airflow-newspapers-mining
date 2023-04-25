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
country = 'Uruguay'
language = 'Spanish'

months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
          'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

class ElPaisSpider(scrapy.Spider):
    name = 'ElPaisSpider'
    start_urls = ['https://www.elpais.com.uy/']
    allowed_domains = ['elpais.com.uy']

    def parse(self, response):
        news_links = response.xpath('//h2[@class="title"]//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.elpais.com.uy'+link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath('//h2[@class="epigraph"]//text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Pais',
            'language' : language,
            'country': country,
            'link': response.url
        }
        
        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)

class Lr21Spider(scrapy.Spider):
    name = 'Lr21Spider'
    start_urls = ['https://www.lr21.com.uy/']
    allowed_domains = ['lr21.com.uy']

    def parse(self, response):
        news_links = response.xpath('//h2//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.lr21.com.uy' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath('//h2[@class="lead"]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'LR21',
            'language' : language,
            'country': country,
            'link': response.url
        }
        
        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)

class ElObservadorSpider(scrapy.Spider):
    name = 'ElObservadorSpider'
    start_urls = ['https://www.elobservador.com.uy/']
    allowed_domains = ['elobservador.com.uy']

    def parse(self, response):
        news_links = response.xpath('//h2//@href | //h1//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.elobservador.com.uy' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath('//h2[@class="article-deck article__deck"]//text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'El Observador',
            'language' : language,
            'country': country,
            'link': response.url
        }
        
        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)

class LaDiariaSpider(scrapy.Spider):
    name = 'LaDiariaSpider'
    start_urls = ['https://ladiaria.com.uy/']
    allowed_domains = ['ladiaria.com.uy']

    def parse(self, response):
        news_links = response.xpath('//h4//@href | //h3//@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://ladiaria.com.uy' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h1//text()').get()
        epigraph = response.xpath('//div[@class="field-field-noticia-bajada"]//text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'La Diaria',
            'language' : language,
            'country': country,
            'link': response.url
        }
        
        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)

class MontevideoSpider(scrapy.Spider):
    name = 'MontevideoSpider'
    start_urls = ['https://www.montevideo.com.uy/']
    allowed_domains = ['montevideo.com.uy']

    def parse(self, response):
        news_links = response.xpath('//h2/a/@href | //article/a/@href').getall()
        for link in news_links:
            if link[0:5] == 'https':
                yield response.follow(url=link, callback=self.parse_links)
            else:
                url = 'https://www.montevideo.com.uy' + link
                yield response.follow(url=url, callback=self.parse_links)

    def parse_links(self, response):
        title = response.xpath('//h2[@class="title"]/text()').get()
        epigraph = response.xpath('//div[@itemprop="description"]/text()').get()

        temp = {
            'title': title,
            'epigraph': epigraph,
            'scrape_date': today,
            'newspaper': 'Montevideo',
            'language' : language,
            'country': country,
            'link': response.url
        }
        
        if temp['title'] == None and temp['epigraph'] == None:
            pass
        else:
            my_collection = my_db[country]
            my_collection.insert_one(temp)

def run_ur_spiders():
    configure_logging()
    runner = CrawlerRunner()

    runner.crawl(ElPaisSpider)
    runner.crawl(Lr21Spider)
    runner.crawl(ElObservadorSpider)
    runner.crawl(LaDiariaSpider)
    runner.crawl(MontevideoSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
run_ur_spiders()