import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
 
SQLALCHEMY_DATABASE_URI = 'postgresql://rxqrftayvbnhbn:pu9nZuYHhIxU6kmozzMviFYEMX@ec2-54-243-237-247.compute-1.amazonaws.com:5432/dfat0bklkd56hb' 
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# administrator list
ADMINS = ['contact@harvardchina.org']

TEST = 'yifan1030@gmail.com'

# pagination
POSTS_PER_PAGE = 3
MAX_SEARCH_RESULTS = 50
