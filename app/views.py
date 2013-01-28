import os
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, PostForm, SearchForm, PostPeopleForm
from models import User, ROLE_USER, Post, Panel, Organization, Advisor, Speaker
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
from werkzeug.utils import secure_filename
#from flask.ext.uploads import UploadSet, IMAGES

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.search_form = SearchForm()
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/', methods = ['GET', 'POST'])
def index():
    #hack: some hard coding in pagination
    featured_speakers = Speaker.query.filter_by(featured = True).paginate(1, POSTS_PER_PAGE, False)
    return render_template('index.html',
        title = 'Home',
        featured_speakers = featured_speakers
    )

@app.route('/partners')
def view_partners():
    table_partners = Organization.query.all()
    return render_template('partners.html',
        title = 'HCF Partners',
        partners = table_partners
    )
@app.route('/speakers')
def view_speakers():
    table_speakers = Speaker.query.all()
    return render_template('partners.html',
        title = 'HCF Speakers',
        partners = table_speakers
    )

@app.route('/advisors')
def view_advisors():
    table_advisors = Advisor.query.all()
    return render_template('partners.html',
        title = 'HCF Advisors',
        partners = table_advisors
    )

@app.route('/search', methods = ['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))

@app.route('/search_results/<query>')
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
        query = query,
        results = results)

#below are admin privileges

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/post_blog', methods = ['GET', 'POST'])
@login_required
def post_blog():
    form = PostForm()
    if form.validate_on_submit():
        #TODO: add a dropdown menu instead of having the user type stuff in
        post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user, panel = form.panel.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('post_blog'))

    return render_template('new_post.html',
        title = 'New Post',
        form = form)

#this is the upload extention's upload at work
#photos = UploadSet('photos', IMAGES)
ALLOWED_EXTENSIONS = set(['png','jpg'])
def allowed_file(filename):
    return '.' in filename and\
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/new_speaker', methods=['GET', 'POST'])
def new_speaker():

    form = PostPeopleForm()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                filename=filename))
    return render_template('new_speaker.html',
        title = 'New Speaker',
        form = form
        )



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page = 1):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
        user = user,
        posts = posts)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    elif request.method != "POST":
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html',
        form = form)

