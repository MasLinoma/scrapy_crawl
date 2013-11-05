# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
#-*- coding:utf-8 -*-
from scrapy.item import Item, Field

class htmlItem(Item):
    # define the fields for your item here like:
    # name = Field()
	pass
	#
	category = Field()
	kind = Field()
	name = Field()
	version = Field()
	size = Field()
	updatetime = Field()
	author = Field()
	dltimes = Field()
	legal_dltimes = Field()
	grade = Field()
	commentNums = Field()
	current_time = Field()

	
