from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length
from app.models import User

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    
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
        
class BlogForm(Form):
    post = TextField('post', validators = [Required()])


class PostPeopleForm(Form):
    name = TextAreaField('name', validators=[Required()])
    bio = TextAreaField('bio', validators=[Required()])
    panels = TextAreaField('panels', validators=[Required()])

    def validate(self):
        if not Form.validate(self):
            return False
        person = People.query.filter_by(name = self.name.data).first()
        if person != None:
            self.name.errors.append('This person is already added, please modify the old one instead')
            #TODO: redirect to modifying the old one
            return False


class SearchForm(Form):
    search = TextField('search', validators = [Required()])
