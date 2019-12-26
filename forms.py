from models import Fcuser
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('re_password')])
    re_password = PasswordField('re_password', validators=[DataRequired()])


class LoginForm(FlaskForm):

    class PasswordValid(object): # 페스워드 검증 함수를 만든 것임.
        def __init__(self, message=None):
            self.message = message
        
        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data

            fcuser = Fcuser.query.filter_by(userid=userid).first()
            if fcuser.password != password:
                raise ValueError('Wrong password!')


    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), PasswordValid()])