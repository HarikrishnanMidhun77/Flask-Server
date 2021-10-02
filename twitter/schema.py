from marshmallow import Schema, fields

class TweetSchema(Schema):
  id = fields.Int(required=True)
  id_string=fields.Str()
  tweets_text = fields.Str()
  source = fields.Str()
  source_url = fields.Str()
  likes = fields.Str()
  time = fields.URL()

class TwitterSchema(TweetSchema):
  user_id = fields.Email(required=True)