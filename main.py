import requests
from pymongo import MongoClient


# Reference
# https://velog.io/@jewon119/02.Python-%ED%99%9C%EC%9A%A9-Crawling-MongoDB
client = MongoClient('localhost', 5000) #Connect to Database
invention_db = client.dbsparta #Create database 'invention' and put it on object 'invention_db'
invention_collection = invention_db.invention_collection #Create collection 'invention_collection' and then put it on object 'invention_collection'

invention_list = {'name': None, 'description': None , 'view':None}
invention_collection.insert_many(''' invention information list''' )

#Find specific keyword
# Reference
# https://jinnynote.com/learn/web/%EC%8A%A4%ED%8C%8C%EB%A5%B4%ED%83%80-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%AC%EB%A1%A4%EB%A7%81-db/
key = str(input('Enter keyword'))
same_name = list(invention_db.invention_collection.find({'name':key}))
same_desp = list(invention_db.invention_collection.find({'description':key}))

