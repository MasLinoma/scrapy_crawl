#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
import time
from tongbutui.items import htmlItem

import re,sys

class tongbutuiSpider(BaseSpider):
    """
    用于抓取tongbutui网上的html信息，并存储或到处为json文件
    """
    name = "tongbutui_app"
    allowed_domains = ['tongbu.com/']
    start_urls = [
        'http://app.tongbu.com/',
        ]  

    def printhxs(self,hxs):
	for i in hxs:
		print i.encode('utf-8')
    def parse_one_game(self, response):
	hxs = HtmlXPathSelector(response)
	#print "parse_one_game"
	#self.printhxs(response.meta['game_category'])
	error = hxs.select("//div[@class='error']/text()") or ['ok']	
	if(error[0] != 'ok'):
		item = htmlItem()
		yield item
	else:
		name = hxs.select("//h1/text()").extract()[0]
		category = "game"
		game_category = response.meta['game_category']
	
		info = hxs.select("//div[@class = 'info']/script/text()").extract() or ["get nothing"]
		#get version
		index1 = info[0].find('downversion', 0) + 13
		index2 = info[0].find('</span>', index1)
		version = info[0][index1: index2]

		#get category
		index1 = info[0].find('"_blank">', index2) + 9
		index2 = info[0].find('</a>', index1)
		kind = info[0][index1: index2]
		#get size
		index1 = info[0].find('<p>', index2) + 6
		index2 = info[0].find('</p>',index1)
		size = info[0][index1: index2]

		#get updatetime
		index1 = info[0].find('<p>', index2) + 8
		index2 = info[0].find('</p>', index1)	
		updatetime = info[0][index1: index2]

		#get author
		index1 = info[0].find('">', index2) + 2
		index2 = info[0].find('</a>', index1)
		author = info[0][index1: index2]
		
		info = hxs.select("//div[@class = 'pt3']/script/text()").extract() or ["get nothing"]
		info[0] = info[0].encode('utf-8')	
		#get dltimes and legal_dltimes
		#string1 = u'下载'.encode('utf-8')
		#print string1
		#print string1.decode('utf-8')
#		string1.decode('utf-8')
		index1 = info[0].find(u"下载".encode('utf-8'), 0) + 9
	        index2 = info[0].find(u'万次'.encode('utf-8'), index1)
		#print "index1:%r" % index1
		#print "index2:%r" % index2
		if(index2 == -1):
			#no more than 10000 dltimes
			#get dltimes
			index2 = info[0].find(u'次'.encode('utf-8'), index1)
       			dltimes = info[0][index1: index2]
			dltimes = int(dltimes)
			#get legal_dltimes
			index1 = info[0].find(u"正版".encode('utf-8'), index2) + 9
			index2 = info[0].find(u'次'.encode('utf-8'), index1)
			legal_dltimes = info[0][index1: index2]
			legal_dltimes = int(legal_dltimes)
		else:
			# more than 10000 dltimes
			#get dltimes
			dltimes = info[0][index1: index2]
			dltimes = int(float(dltimes) * 10000)
			#get legal_dltimes
			index1 = info[0].find(u"正版".encode('utf-8'), index2) + 9
			index2 = info[0].find(u'万次'.encode('utf-8'), index1)
			if (index2 == -1):
				index2 = info[0].find(u'次'.encode('utf-8'), index1)
				legal_dltimes = info[0][index1: index2]
				legal_dltimes = int(legal_dltimes)
			else:
				legal_dltimes = info[0][index1: index2]
				legal_dltimes = int(float(legal_dltimes) * 10000)
		
		#print "dltimes:%r" % dltimes
		#print "legal_dltimes%r" % legal_dltimes
		#get grade
		index1 = info[0].find('class="nopf"', 0)
		if(index1 != -1):
			grade = 'none'
		else:
			index1 = info[0].find('"pf">',0) + 5
			index2 = info[0].find('<span>', index1)
			grade = info[0][index1: index2]
	
		#get commentNum
		info = hxs.select("//div[@id='commentver' and @class='subtitle']/span/a/text()").extract() or ["get nothing"]
		info[0]= info[0].encode('utf-8')
		index1 = info[0].find(u"已有".encode('utf-8'), 0) + 6
		index2 = info[0].find(u'条评论'.encode('utf-8'), index1)
		commentNums = info[0][index1: index2]
		commentNums = int(commentNums)	
		#print 'grade:%r' % grade
#		file = open("txt.log", 'rw+')
		#get time
		current_time = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
		
		#construct item
		
	
		#print 'time:%r'% current_time
		#self.printhxs(name[0])
		#print 'commentNums:%r' % commentNums
		#self.printhxs(info[0])
		#print info[0]
#		print "size:%r" % size
#		print "version:%r" % version
#		print "updatetime:%r" % updatetime
#		print "author:%r" % author
#		print str[1: 4]
#		file.write("%s\n"%name)
#		file.close()
	
		log = "category:%r__game_category:%r__name:%r__version:%r__size:%r__updatetime:%r__author:%r__legal_dltimes:%r__dltimes:%r__grade:%r__commentNums:%r__current_time:%r\n"%(category, game_category, name, version, size, updatetime, author, dltimes, legal_dltimes, grade, commentNums, current_time)
		fo = open('tongbutui_app.log','rw+')
		fo.seek(0,2)
		fo.writelines(log)
		fo.close()
		item = htmlItem()
		'''
		item.name = name
		item.category = category
		item.version = version
		item.size = size
		item.updatetime = updatetime
		item.author = author
		item.dltimes = dltimes
		item.legal_dltimes = legal_dltimes
		item.grade = grade
		item.commentNums = commentNums
		item.current_time = current_time
		'''
	
		yield item

    def parse_all_game(self, response):
        hxs = HtmlXPathSelector(response)
	base_url = get_base_url(response)
	#print "parse_all_game"

	urls = hxs.select('//div[@id="content"]/div/div/ul/li/a[@class = "icon"]/@href').extract()
	#self.printhxs(response.meta['game_category'])
	for url in urls[0:]:
		#print url
		request = Request(urljoin_rfc(base_url, url), dont_filter = True, callback = self.parse_one_game)
		request.meta['game_category'] = response.meta['game_category']
		yield request
	#fout = open('test.log','rw+')
	#fout.seek(0,2)
	#fout.writelines('got it!\n')
	
	urls = hxs.select("//a[@class='next']/@href").extract() or ['none']
	if(urls[0] != 'none'):
		
		request_last = Request(urljoin_rfc(base_url, urls[0]), dont_filter = True, callback = self.parse_all_game)
		request_last.meta['game_category'] = response.meta['game_category']
		yield request_last
	#string1 = urls[0]
	#fout.seek(0,2)
	#fout.write(string1)	
	#fout.close()

#handle the response of new requests in category
    def parse_category(self, response):
	hxs = HtmlXPathSelector(response)
	#print 'helloworld'
	base_url = get_base_url(response)
	#get all-download-url
	url = urljoin_rfc(base_url, hxs.select('//div[@class = "app-nav"]/a/@href').extract()[0])
	#print url
	
	#self.printhxs(response.meta['game_category'])
	#item = htmlItem()
	#return item	
	request = Request(url, dont_filter = True,callback = self.parse_all_game)
	request.meta['game_category'] = response.meta['game_category']
	yield request
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
      
        items = []
	totol_game_urls_of_category = []
	#game category name
	game_category = hxs.select("//ul[@id='apppan']/li/a/text()").extract()
	#for i in game_category[0:]:
	#	self.printhxs(i)
	#the game category links
	urls = hxs.select("//ul[@id='apppan']/li/a/@href").extract()or['']
	#base url of the website(tongbutui)
	base_url = get_base_url(response)
	i = 0
	#print 'helloworld'
	#get the totol games list in every category which will be stored in totol_game_urls_of_category
	for category in urls[0:]:
		#print urljoin_rfc(base_url, category)
		#request the url
	#	yield Request(urljoin_rfc(base_url, category), callback = self.parse_category)
		url_temp = urljoin_rfc(base_url, category)
		#print url_temp
		request = Request(url_temp,dont_filter = True , callback = self.parse_category)
		request.meta['game_category'] = game_category[i]
		i = i + 1
		yield request
			
#	for entry in totol_game_urls_of_category[0:]:
#		print entry
	#return items
	#
	'''	
	for url in  urls[0:]:
		items.append(self.make_requests_from_url(url).replace(callback = self.parse_game))	
	'''
	"""
	item = htmlItem()
	item['htmlcontent'] = content
	items.append(item)
	"""
	"""
	for entry0 in urls[0:]:
		print entry0+"\n"
	for entry in category[0:]:
		self.printhxs(entry)
		print "\n"
        """
	"""
        lis = hxs.select('//li')
        for li in lis:
            cl = li.select('@class').extract()

            if len(cl) > 0 and re.match(r'^cat-item\ cat-item-\d{2,3}$', cl[0]):
                cate = li.select('a/text()').extract()[0]
                item = CateItem()
                item['cate'] = cate
                items.append(item)
      	"""
        #return items


"""
class ShellTagSpider(BaseSpider):
"""

"""
    用于抓取shell网上的tag信息，并存储或导出为json文件
"""   
"""
    name = "shelltag"
    allowed_domains = ['shell909090.com']
    start_urls = [
        'http://shell909090.com/blog',
        ]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        items = []
        
        tags = hxs.select('//div[@class="tagcloud"]/a/text()').extract()
        print tags
        items = []
        for tag in tags:
            item = TagItem()
            item['tag'] = tag
            items.append(item)
        
        return items

class ShellBlogSpider(BaseSpider):
"""
"""
    用于抓取blog内容，根据sitemap内容来找到博客链接
"""   
"""
    name = "shellblog"
    allowed_domains = ['shell909090.com']
    start_urls = [
        'http://shell909090.com/blog/sitemap.xml'
        ]
    
    def parse(self, response):
         hxs = HtmlXPathSelector(response)
         urls = hxs.select('//url/loc/text()').extract()
        
         items = []
        
         debug = True
         if debug:
             url = urls[1]
             items.append(self.make_requests_from_url(url).replace(callback=self.parse_blog))
             return items
         for url in urls[1:]:
             items.append(self.make_requests_from_url(url).replace(callback=self.parse_blog))
         return items
    
    def parse_blog(self, response):
        hxs = HtmlXPathSelector(response)

        title = hxs.select('//h1[@class="entry-title"]/text()').extract() or ['']
        time = hxs.select('//time[@class="entry-date"]/text()').extract() or ['']
        blog = hxs.select('//div[@class="entry-content"]').extract() or ['']
        author = hxs.select('//footer/a[1]/text()').extract() or ['']
        cate = hxs.select('//footer/a[2]/text()').extract() or ['']
        tag = hxs.select('//footer/a[3]/text()').extract() or ['']
        comments = hxs.select('//ol[@class="commentlist"]/li').extract() or ['']

        item = BlogItem()
        item['title'] = title[0]
        item['pub_date'] = time[0]
        item['blog'] = blog[0]
        item['cate'] = cate[0]
        item['comments'] = comments
        item['tag'] = tag
        item['author'] = author
        return item

"""
