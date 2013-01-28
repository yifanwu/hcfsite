from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField, FileField, file_allowed, file_required
from flask.ext.wtf import Required, Length
from app.models import User, Entity, Panel

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    passphrase = TextField('passphrase', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    def validate(self):
        if not Form.validate(self):
            return False
        if self.passphrase.data  != "hc4Z0IE":
            self.passphrase.errors.append('Invalid pass phrase, only HCF board members have access.')
            return False
        return True
    
class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
    
    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
        
    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True
        
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

class PostPeopleForm(Form):
    name = TextAreaField('name', validators=[Required()])
    description = TextAreaField('description', validators=[Required()])
    panel = TextAreaField('panel', validators=[Required()])

    def validate(self):
        if not Form.validate(self):
            return False
        person = Entity.query.filter_by(name = self.name.data).first()
        if person != None:
            self.name.errors.append('This person is already added, please modify the old one instead')
            #TODO: redirect to modifying the old one
            return False


class SearchForm(Form):
    search = TextField('search', validators = [Required()])
