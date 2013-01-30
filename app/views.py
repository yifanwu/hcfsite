import os
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, PostForm, SearchForm, PostSpeakerForm, PostPanelForm, PostAdvisorForm
from models import User, ROLE_USER, Post, Panel, Organization, Advisor, Speaker
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS

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
    panels = Panel.query.all()
    return render_template('index.html',
        title = 'Home',
        featured_speakers = featured_speakers,
        panels = panels
    )

@app.route('/agenda')
def view_partners():
    table_partners = Organization.query.all()
    return render_template('agenda.html',
        title = 'HCF Agenda',
        partners = table_partners
    )

@app.route('/partners')
def view_partners():
    table_partners = Organization.query.all()
    return render_template('partners.html',
        title = 'HCF Partners',
        partners = table_partners
    )

#note that partners.html is NOT a copy-paste error!
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
        post = Post(
            body = form.post.data, timestamp = datetime.utcnow(), author = g.user,
            panel = form.panel.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('post_blog'))

    return render_template('new_post.html',
        title = 'New Post',
        form = form)

@app.route('/new_speaker', methods=['GET', 'POST'])
@login_required
def new_speaker():
    form = PostSpeakerForm()
    if form.validate_on_submit():
        post = Speaker(
            name = form.name.data, description = form.description.data,
            img_url = form.img_url.data, title = form.title.data,
            organization = form.organization.data, panel = form.panel.data, featured = form.featured.data,
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post for new speaker is now live!')
        return redirect(url_for('new_speaker'))

    return render_template('new_speaker.html',
        title = 'New Speaker',
        form = form
    )

@app.route('/new_advisor', methods=['GET', 'POST'])
@login_required
def new_advisor():
    form = PostAdvisorForm()
    if form.validate_on_submit():
        post = Advisor(
            name = form.name.data, description = form.description.data,
            img_url = form.img_url.data, title = form.title.data,
            organization = form.organization.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post for new advisor is now live!')
        return redirect(url_for('new_advisor'))

    return render_template('new_advisor.html',
        title = 'New Advisor',
        form = form
    )

@app.route('/new_partner_org', methods=['GET', 'POST'])
@login_required
def new_panel():
    form = PostSpeakerForm()
    if form.validate_on_submit():
        post = Panel(
            name = form.name.data, description = form.description.data, category = form.category.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post for new panel is now live!')
        return redirect(url_for('new_panel'))

    return render_template('new_panel.html',
        title = 'New Panel',
        form = form
    )

@app.route('/new_panel', methods=['GET', 'POST'])
@login_required
def new_panel():
    form = PostPanelForm()
    if form.validate_on_submit():
        post = Panel(
            name = form.name.data, description = form.description.data, category = form.category.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post for new panel is now live!')
        return redirect(url_for('new_panel'))

    return render_template('new_panel.html',
        title = 'New Panel',
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

