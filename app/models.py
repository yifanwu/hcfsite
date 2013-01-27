from hashlib import md5
from app import db
from app import app
import flask.ext.whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

#people table --> advisors + speakers + panel
class People(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    time_added = db.Column(db.DateTime)
    panel_id = db.Column(db.Integer, db.ForeignKey('panel.id'))

#partners --> description + logo + name
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    logo = db.Column(db.String(128), unique = True) #path to photo
    #TODO: add connection to people

#panels --> category + name + description + questions
class Panel(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(64), unique = True)
    category = db.Column(db.String(64), unique=True)
    #TODO: make sure that no cap works for the string
    description = db.Column(db.String)
    logo = db.Column(db.String(128), unique=True) #path to photo

class Post(db.Model):
    __searchable__ = ['body']
    
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    panel = db.Column(db.String(140))

    def __repr__(self):
        return '<Post %r>' % (self.body)
        
whooshalchemy.whoosh_index(app, Post)
