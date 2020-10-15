import datetime

from pymongo import Connection as mongoConnection

from vyperlogix.classes.SmartObject import SmartFuzzyObject

aConnection = mongoConnection('127.0.0.1', 65535)

db = aConnection.posts_database

posts = db.posts

post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"], "date": datetime.datetime.utcnow()}

s_post = SmartFuzzyObject({"author": "Mike", "text": "My second blog post!", "tags": ["mongodb", "python", "pymongo"], "date": datetime.datetime.utcnow()})

posts.save(post)
posts.save(s_post.asPythonDict())

print posts.count()
p = posts.find_one({"author": "Mike"})
print str(p)
for item in posts.find():
    print str(item)
pass