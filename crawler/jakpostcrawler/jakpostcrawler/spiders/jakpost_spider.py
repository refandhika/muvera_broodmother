import scrapy
import re
from jakpostcrawler.htmlparser import strip_tags
from jakpostcrawler.items import JakpostItem

class JakpostSpider(scrapy.Spider):
	name = "jakpost"
	allowed_domains = ["thejakartapost.com"]
	start_urls = [
		"http://www.thejakartapost.com/index"
	]

	def parse(self, response):
		for i in response.xpath('//div[@class="detail-latest"]'):
			item = JakpostItem()
			#Media Label
			item['media'] = 'Jakarta Post'
			#Date
			item['date'] = ''
			#Author
			item['author'] = 'No Author'
			#Editor
			item['editor'] = 'No Editor'
			#Source
			item['source'] = 'No Source'
			#Title
			item['title'] = i.xpath('a[2]/h5').extract()[0]
			item['title'] = strip_tags(item['title'])
			item['title'] = item['title'].replace(u'\u201c', u'"')
			item['title'] = item['title'].replace(u'\u201d', u'"')
			item['title'] = item['title'].replace(u'\u2013', u'-')
			item['title'] = item['title'].replace(u'\u2014', u'-')
			item['title'] = item['title'].replace(u'\u2018', u"'")
			item['title'] = item['title'].replace(u'\u2019', u"'")
			item['title'] = item['title'].replace(u'\u2026', u"...")
			item['title'] = item['title'].replace(u'\u200e', u'')
			item['title'] = re.sub('^\s+', '', item['title'])
			item['title'] = re.sub('\s+$', '', item['title'])
			item['title'] = re.sub('\\xad', '', item['title'])
			item['title'] = re.sub('\\xa0', '', item['title'])
			#Link
			item['link'] = i.xpath('a[2]/@href').extract()[0]
			#Sinopsis
			item['preview'] = i.xpath('p/text()').extract()[0]
			item['preview'] = item['preview'].replace(u'\u201c', u'"')
			item['preview'] = item['preview'].replace(u'\u201d', u'"')
			item['preview'] = item['preview'].replace(u'\u2013', u'-')
			item['preview'] = item['preview'].replace(u'\u2014', u'-')
			item['preview'] = item['preview'].replace(u'\u2018', u"'")
			item['preview'] = item['preview'].replace(u'\u2019', u"'")
			item['preview'] = item['preview'].replace(u'\u2026', u"...")
			item['preview'] = item['preview'].replace(u'\u200e', u'')
			item['preview'] = re.sub('^\s+', '', item['preview'])
			item['preview'] = re.sub('\s+$', '', item['preview'])
			item['preview'] = re.sub('\\xad', '', item['preview'])
			item['preview'] = re.sub('\\xa0', '', item['preview'])

			#Request Page
			request = scrapy.Request(item['link'], callback=self.parse_content, dont_filter=True)
			request.meta['item'] = item
			yield request

	def parse_content(self, response):
		item = response.meta['item']

		#Date
		date_cleaner = response.xpath('//span[@class="day"]/text()').extract()[0]
		date_cleaner = date_cleaner + response.xpath('//span[@class="time"]/text()').extract()[0]
		date_cleaner = re.sub('\| ', '', date_cleaner)
		date_cleaner = re.sub(',', '', date_cleaner)
		date_cleaner = re.sub('^\S+ ', '', date_cleaner)
		date_cleaner = re.sub('\s+$', '', date_cleaner)
		print date_cleaner
		time_chk = ''
		for y in range(len(date_cleaner)-2,len(date_cleaner)):
			time_chk = time_chk + date_cleaner[y]
		item['date'] = re.sub(' \S+$', '', date_cleaner)
		
		tanggal = ''
		bulan = ''
		tahun = ''
		jam = ''

		for y in range(len(item['date'])-13,len(item['date'])-11):
			tanggal = tanggal + item['date'][y]

		tanggal = re.sub('\s', '', tanggal)
		tanggal = str(tanggal).zfill(2)

		for y in item['date']:
			if y.isalpha():
				bulan = bulan + y

		#Convert format bulan to number
		if (bulan == 'January'):
			bulan = '01'
		elif (bulan == 'February'):
			bulan = '02'
		elif (bulan == 'March'):
			bulan = '03'
		elif (bulan == 'April'):
			bulan = '04'
		elif (bulan == 'May'):
			bulan = '05'
		elif (bulan == 'June'):
			bulan = '06'
		elif (bulan == 'July'):
			bulan = '07'
		elif (bulan == 'August'):
			bulan = '08'
		elif (bulan == 'September'):
			bulan = '09'
		elif (bulan == 'October'):
			bulan = '10'
		elif (bulan == 'November'):
			bulan = '11'
		elif (bulan == 'December'):
			bulan = '12'

		for y in range(len(item['date'])-10,len(item['date'])-6):
			tahun = tahun + item['date'][y]

		if (time_chk == "am") :
			for y in range(len(item['date'])-5,len(item['date'])):
				jam = jam + item['date'][y]
		elif (time_chk == "pm") :
			for y in range(len(item['date'])-5,len(item['date'])-3):
				jam = jam + item['date'][y]
			jam = int(jam) + 12
			jam = str(jam)
			for y in range(len(item['date'])-3,len(item['date'])):
				jam = jam + item['date'][y]

		item['date'] = tahun + '-' + bulan + '-' + tanggal + ' ' + jam + ":00"

		#Content
		pc = 0
		text_sum = response.xpath('//*[@id="show-bubb-text"]/p').extract()[0]
		text_sum = strip_tags(text_sum)
		text_check = response.xpath('//*[@id="show-bubb-text"]/p').extract()[pc]
		for p in response.xpath('//*[@id="show-bubb-text"]/p/text()') :
			if (text_sum == text_check) :
				pc = pc + 1
			elif (text_sum != text_check) :
				pc = pc + 1
				try:
					text_check = response.xpath('//*[@id="show-bubb-text"]/p/text()').extract()[pc]
				except:
					pass
				text_sum = text_sum + " " + text_check
		
		text_cleaner = strip_tags(re.sub('[\t\n\r\f\v]', '', text_sum))
		text_cleaner = text_cleaner.replace(u'\u201c', u'"')
		text_cleaner = text_cleaner.replace(u'\u201d', u'"')
		text_cleaner = text_cleaner.replace(u'\u2013', u'-')
		text_cleaner = text_cleaner.replace(u'\u2014', u'-')
		text_cleaner = text_cleaner.replace(u'\u2018', u"'")
		text_cleaner = text_cleaner.replace(u'\u2019', u"'")
		text_cleaner = text_cleaner.replace(u'\u2026', u"...")
		text_cleaner = text_cleaner.replace(u'\u200e', u'')
		text_cleaner = re.sub('^\s+', '', text_cleaner)
		text_cleaner = re.sub('\s+$', '', text_cleaner)
		text_cleaner = re.sub('\\xad', '', text_cleaner)
		text_cleaner = re.sub('\\xa0', '', text_cleaner)

		#Editor
		try :
			item['editor'] = re.search('\((.{1,3})\)$', text_cleaner).group(1)
		except :
			pass
		#Author
		try :
			item['author'] = response.xpath('//span[@class="name-post"]/text()').extract()[0]
			item['author'] = re.sub('^\s+', '', item['author'])
			item['author'] = re.sub('\s+$', '', item['author'])
		except :
			pass
		#Content Only
		item['cont'] = re.sub('\.\s+\(.+\)$', '.', text_cleaner)

		#Opening
		opening_formula = re.compile(ur'\s*[A-Z].+?\.')
		temp = re.findall(opening_formula,item['cont'])
		if len(temp) >= 4:
			opening = str(temp[0])+str(temp[1])+str(temp[2])+str(temp[3])
		elif len(temp) == 3:
			opening = str(temp[0])+str(temp[1])+str(temp[2])
		elif len(temp) == 2:
			opening = str(temp[0])+str(temp[1])
		elif len(temp) == 1:
			opening = str(temp[0])
		else :
			opening = 'No Content'
		item['opening'] = opening

		#Quote
		quote_formula = re.compile(ur'\"[A-Z].+?[\,\.]+?\".+?\.')
		quote1 = ''
		quote2 = ''
		quote3 = ''
		quote4 = ''
		quote5 = ''

		temp = re.findall(quote_formula,item['cont'])
		if len(temp) >= 5:
			quote1 = str(temp[0])
			quote2 = str(temp[1])
			quote3 = str(temp[2])
			quote4 = str(temp[3])
			quote5 = str(temp[4])
		elif len(temp) == 4:
			quote1 = str(temp[0])
			quote2 = str(temp[1])
			quote3 = str(temp[2])
			quote4 = str(temp[3])
		elif len(temp) == 3:
			quote1 = str(temp[0])
			quote2 = str(temp[1])
			quote3 = str(temp[2])
		elif len(temp) == 2:
			quote1 = str(temp[0])
			quote2 = str(temp[1])
		elif len(temp) == 1:
			quote1 = str(temp[0])
		else:
			quote1 = "No Quote"
		item['quote1'] = quote1
		item['quote2'] = quote2
		item['quote3'] = quote3
		item['quote4'] = quote4
		item['quote5'] = quote5

		yield item
