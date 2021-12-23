import requests
import pymongo


# Reference
# https://velog.io/@jewon119/02.Python-%ED%99%9C%EC%9A%A9-Crawling-MongoDB
conn = pymongo.MogoClient() #Connect to Database
invention_db = conn.invention #Create database 'invention' and put it on object 'invention_db'
invention_collection = invention_db.invention_collection #Create collection 'invention_collection' and then put it on object 'invention_collection'

invention_collection.insert_many(''' invention information list''' )

