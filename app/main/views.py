from flask import render_template,request,redirect,url_for,abort
from .import main
from flask_login import login_required,current_user
from .forms import UpdateProfile,BlogForm,CommentForm
from ..import db,photos
from ..models import User,Blog,Comments
from ..email import mail_message
from ..requests import get_quote
@main.route('/')

def index():
    """
    """
    user=current_user
    blogs=Blog.get_all_blog()
    
    
    title="Blog App"
    message="Welcome to blog app"

    quote = get_quote()
    return render_template('index.html',title=title,message=message,user=user,blogs=blogs, quote=quote)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs=Blog.query.filter_by(user_id=user.id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,blogs=blogs)

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

@main.route('/user/blog/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
    form = BlogForm()
    user=User.get_user(id)
    # users=User.get_all_users()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        # Updated review instance
        new_blog = Blog(title=title,description=description,user_id=user.id)
        mail_message(f"Hello {user.username} You Just Made a post!","email/subscription_new_blog",user.email,user=user)

        # save review method
        new_blog.save_blog()
        return redirect(url_for('.index'))

    title = 'New Blog '
    return render_template('new_blog.html',title = title, form=form,user=user )

@main.route('/user/blog/newcomment/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    user=current_user
    blog=Blog.query.filter_by(id=id).first()
    if form.validate_on_submit():
        comment = form.comment.data 

        # Updated review instance
        new_comment = Comments(comment=comment,blog_id=blog.id,user_id=user.id)

        # save review method
        new_comment.save_comment()
        return redirect(url_for('.blog',id=id))

    title = 'New Blog '
    return render_template('new_comment.html',title = title, form=form,user=user )


@main.route('/blog/<int:id>',methods=['GET','POST'])
def blog(id):

    '''
    View movie page function that returns the movie details page and its data
    '''
    form = CommentForm()
    user=current_user
    blog = Blog.query.filter_by(id=id).first()
    
    if form.validate_on_submit():
        comment = form.comment.data 

        # Updated review instance
        new_comment = Comments(comment=comment,blog_id=blog.id,user_id=user.id)

        # save review method
        new_comment.save_comment()
        return redirect(url_for('main.blog',id=id))
    
    # comments=Comments.query.filter_by(blog_id=id).all()
    
    title = f'{blog.title}'
    return render_template('blog.html',title = title,blog=blog,form=form)

@main.route('/comment/delete/<int:id>')
@login_required
def delete_comment(id):
    """
    """
    form=BlogForm()
    get_comment=Comments.query.filter_by(id=id).first()

    comment=Comments.delete_comment(get_comment.id)

    return redirect(url_for('blog.html',id=get_comment.blog_id,form=form))