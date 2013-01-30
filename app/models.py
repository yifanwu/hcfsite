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


class Entity(db.Model):
    __searchable__ = ['description']

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    description = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String(140), nullable=True)
    entity_type = db.Column(db.String(32), nullable=False)
    __mapper_args__ = {'polymorphic_on': entity_type}

class Advisor(Entity):
    __tablename__ = 'advisor'

    __mapper_args__ = {'polymorphic_identity': 'advisor'}
    id = db.Column(db.Integer, db.ForeignKey('entity.id'), primary_key=True)
    title = db.Column(db.String(140))
    organization = db.Column(db.String(140))

class Speaker(Entity):
    __tablename__ = 'speaker'
    __mapper_args__ = {'polymorphic_identity': 'speaker'}
    id = db.Column(db.Integer, db.ForeignKey('entity.id'), primary_key=True)
    title = db.Column(db.String(140))
    organization = db.Column(db.String(140))
    panel = db.Column(db.String(140))
    featured = db.Column(db.Boolean)

class Organization(Entity):
    __tablename__ = 'organization'
    __mapper_args__ = {'polymorphic_identity': 'organization'}
    id = db.Column(db.Integer, db.ForeignKey('entity.id'), primary_key=True)

class Panel(Entity):
    __tablename__ = 'panel'
    __mapper_args__ = {'polymorphic_identity': 'panel'}
    id = db.Column(db.Integer, db.ForeignKey('entity.id'), primary_key=True)
    category = db.Column(db.String(64), unique=True)

class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['body']
    
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    panel = db.Column(db.String(140))

    def __repr__(self):
        return '<Post %r>' % (self.body)
        
whooshalchemy.whoosh_index(app, Post)
