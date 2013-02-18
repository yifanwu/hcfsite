from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField, SelectField
from flask.ext.wtf import Required, Length, URL, Email
from flask.ext.wtf.html5 import URLField
from app.models import User, Panel, Advisor, Speaker, Organization, Group

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    passphrase = TextField('passphrase', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    def validate(self):
        if not Form.validate(self):
            return False
        if self.passphrase.data  != "hcf2013admin":
            self.passphrase.errors.append('Invalid pass phrase, only HCF board members have access.')
            return False
        return True

class EditForm(Form):
    name = TextField('name', validators=[Required()])
    description = TextAreaField('description', validators=[Required()])
    panel = SelectField(u'panel', coerce=int)
    #TextAreaField('panel', validators=[Required()])
    featured = BooleanField('featured', default = False)
    img_url = URLField(validators=[URL()])
    title = TextAreaField('title', validators=[Required()])
    organization = TextAreaField('organization', validators=[Required()])

    def validate(self):
        if not Form.validate(self):
            return False
        if self.name == None:
            self.name.errors.append('This is an invalid entry!')
            return False
        return True

class ContactForm(Form):
    name = TextField('name', validators=[Required()])
    subject = TextField('subject', validators=[Required()])
    email_add = TextField('email_add', validators=[Required()])
    msg = TextAreaField('msg', validators=[Required()])

class PostForm(Form):
    post = TextField('post', validators = [Required()])
    panel = TextField('panel', validators = [Required()])

    def validate(self):
        if not Form.validate(self):
            return False
        panel_id = Panel.query.filter_by(name = self.panel.data)
        if panel_id == None:
            self.panel.errors.append('This panel does not yet exist in the database, please check for typo or add panel')
            return False
        return True

class PostGroupForm(Form):
    name = TextField('name', validators=[Required()])
    description = TextAreaField('description', validators=[Required()])
    def validate(self):
        return True

class PostCategoryForm(Form):
    name = TextField('name', validators=[Required()])

class PostTeamForm(Form):
    name = TextField('name', validators=[Required()])
    description = TextAreaField('description', validators=[Required()])
    title = TextField('title', validators=[Required()])
    email = TextField('Email', validators=[Email()])
    img_url = URLField(validators=[URL()])
    group_id = SelectField(u'group_id', coerce=int)

class PostSpeakerForm(Form):
    name = TextField('name', validators=[Required()])
    description = TextAreaField('description', validators=[Required()])
    panel_id = SelectField(u'panel_id', coerce=int)
    featured = BooleanField('featured', default = False)
    img_url = URLField(validators=[URL()])
    title = TextAreaField('title', validators=[Required()])
    organization = TextAreaField('organization', validators=[Required()])

    def validate(self):
        if not Form.validate(self):
            self.name.errors.append('Something went wrong!')
            return False
        person = Speaker.query.filter_by(name = self.name.data).first()
        if person != None:
            self.name.errors.append('This speaker is already added, please modify the old one instead')
            return False
        return True

class PostAdvisorForm(Form):
    name = TextField('name', validators=[Required()])
    description = TextAreaField('description', validators=[Required()])
    img_url = URLField(validators=[URL()])
    title = TextField('title', validators=[Required()])
    organization = TextField('organization', validators=[Required()])

    def validate(self):
        if not Form.validate(self):
            self.name.errors.append('Something went wrong!')
            return False
        person = Advisor.query.filter_by(name = self.name.data).first()
        if person != None:
            self.name.errors.append('This advisor is already added, please modify the old one instead')
            return False
        return True

class PostOrganizationForm(Form):
    name = TextAreaField('name', validators=[Required()])
    description = TextAreaField('description', validators=[Required()])
    img_url = URLField(validators=[URL()])

    def validate(self):
        if not Form.validate(self):
            return False
        found_name = Organization.query.filter_by(name = self.name.data).first()
        if found_name != None:
            self.name.errors.append('This panel is already added, please modify the old one instead')
            return False
        return True

class PostPanelForm(Form):
    name = TextAreaField('name', validators=[Required()])
    description = TextAreaField('description', validators=[Required()])
    keyq = TextAreaField('keyq', validators=[Required()])

    category_id = SelectField('category_id', coerce=int)

    def validate(self):
        if not Form.validate(self):
            return False
        found_name = Panel.query.filter_by(name = self.name.data).first()
        if found_name != None:
            self.name.errors.append('This panel is already added, please modify the old one instead')
            return False
        return True

class SearchForm(Form):
    search = TextField('search', validators = [Required()])
