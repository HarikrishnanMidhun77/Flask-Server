import os
from pymongo import MongoClient

COLLECTION_NAME = 'twitter'

class MongoRepository(object):
  def __init__(self):
    mongo_url = 'mongodb+srv://harikrishnan_midhun2:DM_pswd@cluster0.iwigi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    self.db = MongoClient(mongo_url).twitter

  def find_all(self, selector):
    return self.db.twitter.find(selector)
 
  def find(self, selector):
    return self.db.twitter.find_one(selector)
 
  def create(self, kudo):
    return self.db.twitter.insert_one(kudo)

  def update(self, selector, kudo):
    return self.db.twitter.replace_one(selector, kudo).modified_count
 
  def delete(self, selector):
    return self.db.twitter.delete_one(selector).deleted_count