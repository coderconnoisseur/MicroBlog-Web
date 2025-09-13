from Projectdir import db, login
from time import time
import jwt
from flask import current_app  # Changed from 'from Projectdir import app'
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from hashlib import md5
from Projectdir.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total
    @classmethod
    def before_commit(cls, session):
        session._changes = {
        'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None
    
    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # Remove duplicate posts relationship
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User', secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    __searchable__ = ['body']
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0
    
    def followed_posts(self):
        followed= Post.query.join(
            followers,(followers.c.followed_id==Post.user_id)).filter(followers.c.follower_id==self.id)
        own=Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    
    def following_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
        
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)
    
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],  # Changed from app.config
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            data = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'],  # Changed from app.config
                algorithms=['HS256']
            )
        except:
            return
        return User.query.get(data['reset_password'])
class Post(SearchableMixin, db.Model):
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Remove duplicate relationship definition
    
    def __repr__(self):
        return f'Post {self.body} and {self.id}'
      # Fixed to use data['reset_password']


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)