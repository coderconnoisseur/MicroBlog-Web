from Projectdir import app,db,login
from flask import render_template , redirect,flash,url_for,request
from Projectdir.forms import LoginForm ,EditProfileForm,EmptyForm,PostForm,ResetPasswordRequestForm,RegistrationForm,ResetPasswordForm
from flask_login import current_user,login_user,logout_user,login_required
from Projectdir.models import User,Post
from urllib.parse import urlparse
from Projectdir.email import send_password_reset_email
from datetime import datetime   


@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(body=form.post.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post is now live!!!')
        return redirect(url_for('index'))
    page=request.args.get('page',1,type=int)
    posts=current_user.followed_posts().paginate(page=page,per_page=app.config['POSTS_PER_PAGE'],
                                                error_out=False)
    next_url=url_for('index',page=posts.next_num) \
        if posts.has_next else None
    prev_url=url_for('index',page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html',
                        title="Home Page",
                        form=form,
                        posts=posts.items,
                        next_url=next_url,
                        prev_url=prev_url)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('INVALID USERNAME OR PASSWORD')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',form = form,title = 'Sign in')
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user.')
        return redirect(url_for('login'))
    return render_template('register.html',form=form,title = 'register')

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page=request.args.get('page',1,type=int)
    posts=user.posts.order_by(Post.timestamp.desc()).paginate(page=page,per_page=app.config["POSTS_PER_PAGE"],error_out=False)
    next_url=url_for('user',username=user.username,page=posts.next_num)\
        if posts.has_next else None
    prev_url=url_for('user',username=user.username,page=posts.prev_num)\
        if posts.has_prev else None
    form=EmptyForm()
    return render_template('user.html',user=user,form=form,next_url=next_url,prev_url=prev_url,posts=posts.items)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen=datetime.utcnow()
        db.session.commit()
        
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)

@login_required
@app.route('/follow/<username>',methods=['POST'])
def follow(username):
    form=EmptyForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=username).first()
        if user is None:
            flash('User {}not found'.format(username))
            return redirect(url_for('user', username=username))
        if user==current_user:
            flash("You cannot follow yourself")
            return redirect(url_for('user',username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}'.format(username))
        return redirect(url_for('user',username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>',methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found'.format(username))
            return redirect(url_for('index'))
        if user==current_user:
            flash('You cannot unfollow yourself')
            return redirect(url_for('user',username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}'.format(username))
        return redirect(url_for('user',username=username))
    else:
        return redirect(url_for('index'))
    
@app.route('/Explore')
@login_required
def Explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    next_url = url_for('Explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('Explore', page=posts.prev_num) if posts.has_prev else None
    
    # Debugging prints
    print(f"Current page: {page}")
    print(f"Has previous page: {posts.has_prev}")
    print(f"Has next page: {posts.has_next}")
    print(f"Previous page number: {posts.prev_num}")
    print(f"Next page number: {posts.next_num}")
    
    return render_template('index.html',
                        title='Explore',
                        posts=posts.items,
                        next_url=next_url,
                        prev_url=prev_url)
    
    
@app.route('/reset_password_request',methods=['GET',"POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for instructions to reset your password")
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',title='Reset Password',form=form)

@app.route('/reset_password/<token>',methods=["GET","POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user=User.verify_reset_password_token(token=token)
    if not user:
        return redirect(url_for('index'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your Password has been reset!!!")
        return redirect(url_for('login'))
    return render_template('reset_password.html',form=form)

        