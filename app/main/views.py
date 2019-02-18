from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import Post, User, Comment, Upvote, Downvote
from .forms import PostForm, CommentForm, UpvoteForm, UpdateProfile
from flask.views import View, MethodView
from .. import db, photos
import markdown2


# Views
@main.route('/', methods=['GET', 'POST'])
def index():
    '''
    View root page function that returns the index page and its data
    '''
    # post = Post.query.filter_by().first()
    title = 'Home'
    businesspost= Post.query.filter_by(category="businesspost")
    interviewpost = Post.query.filter_by(category="interviewpost")
    techpost = Post.query.filter_by(category="techpost")
    pickuppost = Post.query.filter_by(category="pickuppost")

    # upvotes = Upvote.get_all_upvotes(post_id=Post.id)

    return render_template('index.html', title=title, pickuppost=pickuppost,
                           interviewpost=interviewpost, businesspost=businesspost, techpost=techpost, blog = Post.query.all() )



@main.route('/pickup', methods=['GET', 'POST'])
def pickup():
    post = Post.query.filter_by().first()
    pickuppost = Post.query.filter_by(category="pickuppost")
    return render_template('pickup.html', post=post, pickuppost=pickuppost)

@main.route('/business', methods=['GET', 'POST'])
def business():
    post = Post.query.filter_by().first()
    businesspost= Post.query.filter_by(category="businesspost")

    return render_template('business.html', businesspost=businesspost, post=post)

@main.route('/interview', methods=['GET', 'POST'])
def interview():
    post = Post.query.filter_by().first()
    interviewpost = Post.query.filter_by(category="interviewpost")

    return render_template('interview.html', post=post, interviewpost=interviewpost)

@main.route('/technology', methods=['GET', 'POST'])
def technology():
    techpost = Post.query.filter_by(category="techpost")
    post = Post.query.filter_by().first()
    return render_template('technology.html', post=post, techpost=techpost)

@main.route('/posts', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    my_upvotes = Upvote.query.filter_by(post_id=Post.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_post = Post(owner_id=current_user._get_current_object().id, title=title, description=description,
                          category=category)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('posts.html', form=form)


@main.route('/comment<int:post_id>', methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description=description, user_id=current_user._get_current_object().id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment', post_id=post_id))

    all_comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('comments.html', form=form, comment=all_comments, post=post)


@main.route('/post/upvote/<int:post_id>/upvote', methods=['GET', 'POST'])
@login_required
def upvote(post_id):
    post = Post.query.get(post_id)
    user = current_user
    post_upvotes = Upvote.query.filter_by(post_id=post_id)

    if Upvote.query.filter(Upvote.user_id == user.id, Upvote.post_id == post_id,post=post).first():
        return redirect(url_for('main.index'))

    new_upvote = Upvote(post_id=post_id, user=current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))


@main.route('/post/downvote/<int:post_id>/downvote', methods=['GET', 'POST'])
@login_required
def downvote(post_id):
    post = Post.query.get(post_id)
    user = current_user
    post_downvotes = Downvote.query.filter_by(post_id=post_id)

    if Downvote.query.filter(Downvote.user_id == user.id, Downvote.post_id == post_id).first():
        return redirect(url_for('main.index'))

    new_downvote = Downvote(post_id=post_id, user=current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))



@main.route('/profile/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))