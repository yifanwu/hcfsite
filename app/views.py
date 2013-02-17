import os
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, PostForm, SearchForm, PostSpeakerForm, PostPanelForm, \
    PostAdvisorForm, PostOrganizationForm, PostCategoryForm, PostTeamForm, PostGroupForm
from models import User, ROLE_USER, Post, Panel, Organization, Advisor, Speaker, Category, Team, Group
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
from flask import request

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
    cat_list = Category.query.all()

    for cat in cat_list:
        cat.html_id = "cat_" + str(cat.id)

    return render_template('index.html',
        title = 'Home',
        page_id = 'home',
        featured_speakers = featured_speakers,
        panels = panels,
        categories = cat_list
    )

@app.route('/agenda')
def view_agenda():
    return render_template('agenda.html',
        title = 'HCF Agenda',
        page_id = 'agenda'
    )

@app.route('/team')
def view_team():
    table_team  = Team.query.all()
    table_group = Group.query.all()
    return render_template('team.html',
        title   = 'HCF Team',
        page_id = 'team',
        partners = table_team,
        group   = table_group,
        type    = 'team'
    )

@app.route('/partners')
def view_partners():
    table_partners = Organization.query.all()
    return render_template('partners.html',
        title = 'HCF Partners',
        page_id = 'partners',
        partners = table_partners,
        type = 'partner'
    )

@app.route('/logistics')
def view_logistics():
    return render_template('logistics.html',
        title = 'Logistics',
        page_id = 'logistics'
    )

@app.route('/about')
def view_about():
    return render_template('about.html',
        title = 'About HCF',
        page_id = 'about'
    )

#note that partners.html is NOT a copy-paste error!
@app.route('/speakers')
def view_speakers():
    table_speakers = Speaker.query.all()
    cat_list = Category.query.all()
    panel_list = Panel.query.all()

    for panel in panel_list:
        panel.html_id = "panel_" + str(panel.id)
        panel.speakers_list = [[], []]
        i = 0
        for speaker in table_speakers:
            if speaker.panel_id == panel.id:
                panel.speakers_list[i % 2].append(speaker)
                speaker.edit_url = "edit/speaker/" + str(speaker.id)
                i += 1

    return render_template('speakers.html',
        title = 'HCF Speakers',
        page_id = 'speakers',
        type = 'speaker',
        panels = panel_list,
        categories = cat_list
    )

@app.route('/panels')
def view_panels():
    cat_list    = Category.query.all()
    panel_list  = Panel.query.all()

    for cat in cat_list:
        cat.html_id = "cat_" + str(cat.id)

    for panel in panel_list:
        panel.html_id = "panel_" + str(panel.id)

    return render_template('panels.html',
       title = 'HCF Panels',
       page_id = 'panels',
       type = 'panel',
       panels = panel_list,
       categories = cat_list
    )

@app.route('/advisors')
def view_advisors():
    table_advisors = Advisor.query.all()
    length = len(table_advisors)
    advisors_list = [table_advisors[:length / 2], table_advisors[(length / 2):]]
    return render_template('advisors.html',
        title = 'HCF Advisors',
        page_id = 'advisors',
        advisors_list = advisors_list,
        type = 'advisor'
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
        results = results
    )

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

@app.route('/new_category', methods=['GET', 'POST'])
@login_required
def new_category():
    form = PostCategoryForm()

    if form.validate_on_submit():
        post = Category(name = form.name.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post for new CATEGORY is now lIVE!')
        return redirect(url_for('new_category'))
    return render_template('new_category.html',
        title = 'New Category',
        form = form,
    )


@app.route('/new_group', methods=['GET', 'POST'])
@login_required
def new_group():
    form = PostGroupForm()

    if form.validate_on_submit():
        post = Group(name = form.name.data, description =
                form.description.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post for new GROUP now lIVE!')
        return redirect(url_for('new_group'))
    return render_template('new_group.html',
        title = 'New Group',
        form = form,
    )

@app.route('/new_team', methods=['GET', 'POST'])
@login_required
def new_team():
    form        = PostTeamForm()
    group_list  = Group.query.all()
    form.group_id.choices = [(g.id, g.name) for g in group_list]

    if form.validate_on_submit():
        post = Team(name = form.name.data, bio = form.bio.data, img_url
                = form.img_url.data, group_id = form.group_id.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post for new TEAM is now lIVE!')
        return redirect(url_for('new_team'))
    return render_template('new_team.html',
        title = 'New Team',
        form = form,
    )

@app.route('/new_speaker', methods=['GET', 'POST'])
@login_required
def new_speaker():
    form = PostSpeakerForm()
    panel_list = Panel.query.all()
    form.panel_id.choices = [(g.id, g.name) for g in panel_list]

    if form.validate_on_submit():
        post = Speaker(
            name = form.name.data, description = form.description.data,
            img_url = form.img_url.data, title = form.title.data,
            organization = form.organization.data, panel_id = form.panel_id.data, featured = form.featured.data,
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post for new speaker is now live!')
        return redirect(url_for('new_speaker'))

    return render_template('new_speaker.html',
        title = 'New Speaker',
        form = form,
        panels = panel_list,

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



@app.route('/new_panel', methods=['GET', 'POST'])
@login_required
def new_panel():
    form = PostPanelForm()
    categories = Category.query.all()
    form.category_id.choices = [(g.id, g.name) for g in categories]

    if form.validate_on_submit():
        post = Panel(
            name = form.name.data, info = form.info.data, category_id =
            form.category_id.data, keyq = form.keyq.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post for new panel is now live!')
        return redirect(url_for('new_panel'))

    return render_template('new_panel.html',
        title = 'New Panel',
        form = form,
        categories = categories
    )

@app.route('/new_partner_org', methods=['GET', 'POST'])
@login_required
def new_partner_org():
    form = PostOrganizationForm()
    if form.validate_on_submit():
        post = Organization(
            name = form.name.data, description = form.description.data, img_url = form.img_url.data,
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post for new partner is now live!')
        return redirect(url_for('new_partner_org'))

    return render_template('new_partner.html',
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

map_tab = {'speaker':Speaker, 'panel':Panel, 'advisor':Advisor,
           'organization': Organization, 'group':Group,
           'category':Category}

@app.route('/how_to', methods = ['GET'])
def how_to():
    return render_template('how_to.html')

#the variables are string by default
@app.route('/edit/<table>/<id>', methods = ['GET', 'POST'])
@login_required
def edit_entity(table, id):

    to_edit = map_tab[table].query.filter_by(id = id).first()
    form = EditForm()

    form.populate_obj(to_edit)

    '''
    form = EditForm("POST", obj=to_edit)

    if entity_content == None:
        flash("This entity doesn\'t exit!")
    if request.POST and form.validate():
        form.populate_obj(to_edit)
        to_edit.save()
        return redirect('/')
    '''
    #return render_to_response('edit_profile.html', form=form)

    '''
    im form.validate_on_submit():
        for i, field in enumerate(form):
            entity_content[i] = field.data


        entity_content.name = form.name.data
        entity_content.description = form.description.data
        entity_content.img_url = form.img_url.data
        if table == 'advisor' or table == 'speaker':
            entity_content.title = form.title.data
            entity_content.organization = form.organization.data
            if table == 'speaker':
                entity_content.panel = form.panel.data
                entity_content.featured = form.featured.data

        db.session.commit()

    elif request.method != "POST":
        form = entity_content
        #for i, field in enumerate(form):
         #   field.data = entity_content[i]


        form.name.data = entity_content.name
        form.description.data = entity_content.description
        form.img_url.data = entity_content.img_url
        if table == 'advisor' or table == 'speaker':
            form.title.data = entity_content.title
            form.organization.data = entity_content.organization
            if table == 'speaker':
                form.panel.data = entity_content.panel
                form.featured.data = entity_content.featured# I CANNOT DO .ITEM HERE BECAUSE IT'S A STRING
    '''
    return render_template('edit_entity.html',
        form = form,
        table = table,
        id = id,
    )


