from ..repository import Repository
from ..repository.mongo import MongoRepository
from .schema import TweetSchema

class Service(object):
  def __init__(self, user_id, repo_client=Repository(adapter=MongoRepository)):
    self.repo_client = repo_client
    self.user_id = user_id

    if not user_id:
      raise Exception("user id not provided")

  def find_all_tweets(self):
    tweets  = self.repo_client.find_all({'user_id': self.user_id})
    return [self.dump(tweet) for tweet in tweets]

  def find_kudo(self, tweet_id):
    tweet = self.repo_client.find({'user_id': self.user_id, 'tweet_id': tweet_id})
    return self.dump(tweet)

  def create_kudo_for(self, twitterTweet):
    self.repo_client.create(self.prepare_kudo(twitterTweet))
    return self.dump(twitterTweet.data)

  def update_kudo_with(self, tweet_id, twitterTweet):
    records_affected = self.repo_client.update({'user_id': self.user_id, 'tweet_id': tweet_id}, self.prepare_kudo(twitterTweet))
    return records_affected > 0

  def delete_kudo_for(self, tweet_id):
    records_affected = self.repo_client.delete({'user_id': self.user_id, 'tweet_id': tweet_id})
    return records_affected > 0

  def dump(self, data):
    return TweetSchema(exclude=['_id']).dump(data).data

  def prepare_kudo(self, twitterTweet):
    data = twitterTweet.data
    data['user_id'] = self.user_id
    return data