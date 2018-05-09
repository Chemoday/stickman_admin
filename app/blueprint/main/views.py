from flask import render_template, session, \
    redirect, url_for, current_app, flash, request, make_response

from . import main_bp
from .forms import NameForm
from app.models.models import User

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        User.create(username=form.name.data)
        return url_for('.index')
    return render_template('index.html', form=form)

