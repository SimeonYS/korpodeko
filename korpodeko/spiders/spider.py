import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import KorpodekoItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class KorpodekoSpider(scrapy.Spider):
	name = 'korpodeko'
	start_urls = ['https://korpodeko.cw/category/press/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="entire-meta-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):

		date = response.xpath('//div[@class="wrap"]/h6/text()').get()
		title = response.xpath('//h1[@class="entry-title"]/text()').get()
		content = response.xpath('//div[contains(@id,"fws_")][2]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=KorpodekoItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
