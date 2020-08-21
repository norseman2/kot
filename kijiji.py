import json

import feedparser
import sys
import requests
import boto3
from datetime import datetime

def getFeedItems(url):
	kFeed = feedparser.parse(url)
	print(kFeed)
	feedItems = kFeed.entries
	return feedItems

def getRealEstateSales(feedItems):
	sales = []
	cpt=0
	for item in feedItems:
		print(item)
		'''
		sale = {}
		url = item.link
		urlParts = url.split('/')
		kijijiId = urlParts[-1]
		rental["kijiji_id"] = int(kijijiId)
		rental["url"] = url
		rental["title"] = item.title
		rental["description"] = item.summary
		updated = item.updated.replace('Z','')
		updated = updated.replace('T',' ')
		rental["published"] = updated
		rental["published_year"] = getYear(updated)
		rental["published_month"] = getMonth(updated)
		rental["published_day"] = getDay(updated)
		rental["published_dayofweek"] = getDayOfWeek(updated)
		rental["published_hour"] = getHour(updated)
		rental["published_weeknumber"] = getWeekNumber(updated)
		rental["published_dayofyear"] = getDayOfYear(updated)
		if "g-core_price" in item.keys():
			rental["price"] = item["g-core_price"]
		else:
			rental["price"] = 0
		if "geo_lat" in item.keys():
			rental["geo_latitude"] = item["geo_lat"]
		else:
			rental["geo_latitude"] = 0
		if "geo_long" in item.keys():
			rental["geo_longitude"] = item["geo_long"]
		else:
			rental["geo_longitude"] = 0
		setHtml(url,rental)
		rentals.append(rental)		
		cpt += 1
		#if(cpt > 1):
		#    break
		'''
	return sales

def getYear(adate):
	dateParts = adate.split(' ')[0].split('-')
	return dateParts[0]

def getMonth(adate):
	dateParts = adate.split(' ')[0].split('-')
	return dateParts[1]

def getDay(adate):
	dateParts = adate.split(' ')[0].split('-')
	return dateParts[2]

def getHour(adate):
	dateParts = adate.split(' ')[1].split(':')
	return dateParts[0]	

def getWeekNumber(adate):
	datetime_object = datetime.strptime(adate, '%Y-%m-%d %H:%M:%S')
	return datetime_object.strftime("%V")

def getDayOfYear(adate):
	datetime_object = datetime.strptime(adate, '%Y-%m-%d %H:%M:%S')
	return datetime_object.strftime("%j")

def getDayOfWeek(adate):
	datetime_object = datetime.strptime(adate, '%Y-%m-%d %H:%M:%S')
	return datetime_object.strftime("%u")

def setHtml(url,rental):
	try:
		page = requests.get(url)
		rental['html'] = page.content.decode()
	except:
		raise


#https://www.kijiji.ca/rss-srp-for-sale/ontario/c30353001l9004
#https://www.kijiji.ca/rss-srp-for-sale/ontario/page-2/c30353001l9004
#https://www.kijiji.ca/rss-srp-for-sale/ontario/page-3/c30353001l9004
feedUrl = "https://www.kijiji.ca/rss-srp-for-sale/ontario/c30353001l9004"
sales = getRealEstateSales(getFeedItems(feedUrl))
print(sales)
#stored = storeRentals(rentals)