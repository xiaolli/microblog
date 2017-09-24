from flask_wtf import Form
from wtforms import StringField,PasswordField,TextAreaField,FileField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
    username=StringField(label='Username',validators=[DataRequired()])
    password=PasswordField(label='Password',validators=[DataRequired()])

class UserForm(Form):
    nickname = StringField(label='nickname',validators=[DataRequired()])
    description= TextAreaField(label='About Me',validators=[Length(min=0,max=140)])
    image = FileField(label='Image')

class NewUserForm(Form):
    username = StringField(label='Username',validators=[DataRequired(message='username is required')])
    password = PasswordField(label='Password',validators=[DataRequired(message='password is required')])
    nickname = StringField(label='Nickname',validators=[DataRequired(message='nickname is required')])
    description = TextAreaField(label='About Me',validators=[Length(min=0,max=140)])

class PostForm(Form):
    post = TextAreaField(label='Post',validators=[Length(min=20,max=500,message='words are less than 20 or more than 500 is not allowed')])

class SearchForm(Form):
    search = StringField(label='Search',validators=[DataRequired(message='Query key is required!')])