# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider
import urlparse
from urlparse import urlparse

class LinkData(scrapy.Item):
	base = scrapy.Field()
	title = scrapy.Field()
	url = scrapy.Field()
	text = scrapy.Field()
	url_title = scrapy.Field()
	keywords = scrapy.Field()
	description = scrapy.Field()
	og_title = scrapy.Field()
	og_description = scrapy.Field()


class JumponSpider(scrapy.Spider):
	
	name = 'jumpcrw'
	
	COUNTER=1


	def __init__(self, WPAGE=None, *args, **kwargs):
		super(JumponSpider, self).__init__(*args, **kwargs)
		self.start_urls = [WPAGE]
		url = urlparse(WPAGE)
		
		self.allowed_domains = [url.netloc]

	def assignValue(self, obj, key, val):
		if val is not None:
			obj[key] = val
		return obj	

	def parse(self, response):
		for link in response.css('a'):           	
		
			linkData = LinkData()
			linkData['base'] = response.url;
			linkData = self.assignValue(linkData, 'url_title', link.css('a::attr(title)').extract_first())
			linkData = self.assignValue(linkData, 'url', link.css('a::attr(href)').extract_first())
			linkData = self.assignValue(linkData, 'text', link.css('a::text').extract_first())
			
			if 'url' in linkData:
				
				request = scrapy.Request(response.urljoin(linkData['url']), callback=self.parse_next_page)
				request.meta['linkData'] = linkData
			
				yield request


	def parse_next_page(self, response):
		link_data = response.meta['linkData']
		link_data = self.assignValue(link_data, 'title', response.css('title::text').extract_first())
		link_data = self.assignValue(link_data, 'keywords', response.xpath('//meta[@name="keywords"]/@content').extract_first())      	
		link_data = self.assignValue(link_data, 'description', response.xpath('//meta[@name="description"]/@content').extract_first())
		
		link_data = self.assignValue(link_data, 'og_title', response.xpath('//meta[@property="og:title"]/@content').extract_first())
		link_data = self.assignValue(link_data, 'og_description', response.xpath('//meta[@property="og:description"]/@content').extract_first())

		#self.COUNTER += 1
		#if self.COUNTER > 10:
		#	raise CloseSpider('bandwidth_exceeded')
		
		
		yield link_data    
            