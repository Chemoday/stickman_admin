
from flask_wtf import FlaskForm
from wtforms import *


class NameForm(FlaskForm):
    name = StringField('Your name?')
    submit = SubmitField('Submit')

