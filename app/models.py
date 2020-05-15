from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(UserMixin,db.Model):

    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    subscription=db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    blog=db.relationship('Blog',backref='user',lazy="dynamic")
    comments=db.relationship('Comments',backref='user',lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    @classmethod
    def get_user(cls,id):
        user=User.query.filter_by(id=id).first()
        return user
    def get_all_users():
        users=User.query.filter_by(subscription==True).all()
        return users
        
    def __repr__(self):
        return f'user {self.username}'
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255))
    users=db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return f'user {self.username}'

class Blog(db.Model):
    __tablename__='blog'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String)
    description=db.Column(db.String)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    comment=db.relationship('Comments',backref='blog',lazy='dynamic')
    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_blog(cls):
        blogs=Blog.query.all()
        return blogs
    def get_blog(cls,id):
        blog=Blog.query.filter_by(id=id).first()
        return blog


    def __repr__(self):
        return f'user {self.title}'

class Comments(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String)
    blog_id=db.Column(db.Integer,db.ForeignKey("blog.id"))
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))


    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_comment(cls,id):
        comment=Comments.query.filter_by(id=id).delete()
        

    def __repr__(self):
        return f'user {self.id}'