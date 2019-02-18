from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import UserMixin, current_user
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    post = db.relationship('Post', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    upvotes = db.relationship('Upvote', backref='user', lazy='dynamic')
    downvotes = db.relationship('Downvote', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'{self.username}'


class Post(db.Model):
    '''
    '''
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(), index=True)
    title = db.Column(db.String())
    category = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    upvotes = db.relationship('Upvote', backref='post', lazy='dynamic')
    downvotes = db.relationship('Downvote', backref='post', lazy='dynamic')

    @classmethod
    def get_posts(cls, id):
        posts = Post.query.order_by(post_id=id).desc().all()
        return posts

    def __repr__(self):
        return f'Post {self.description}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"


class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer, primary_key=True)
    upvote = db.Column(db.Integer, default=1)
    post_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_upvotes(self):
        db.session.add(self)
        db.session.commit()

    def add_upvotes(cls, id):
        upvote_post = Upvote(user=current_user, post_id=id)
        upvote_post.save_upvotes()

    @classmethod
    def get_upvotes(cls, id):
        upvote = Upvote.query.filter_by(post_id=id).all()
        return upvote

    @classmethod
    def get_all_upvotes(cls, post_id):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.post_id}'


class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer, primary_key=True)
    downvote = db.Column(db.Integer, default=1)
    post_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_downvotes(self):
        db.session.add(self)
        db.session.commit()

    def add_downvotes(cls, id):
        downvote_post = Downvote(user=current_user, post_id=id)
        downvote_post.save_downvotes()

    @classmethod
    def get_downvotes(cls, id):
        downvote = Downvote.query.filter_by(post_id=id).all()
        return downvote

    @classmethod
    def get_all_downvotes(cls, post_id):
        downvote = Downvote.query.order_by('id').all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.post_id}'
