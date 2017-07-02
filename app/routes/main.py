from flask import current_app, request, session, url_for, redirect, render_template, flash
from flask_weasyprint import HTML, render_pdf
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import sqlalchemy
from flask_principal import Permission, RoleNeed, Identity, identity_changed, \
     identity_loaded, UserNeed, AnonymousIdentity

from datetime import datetime
from sqlalchemy import desc

from app import app, db, login_manager
from app.models import *
from app.forms import *
from app.constants import MSG

import json, jsonify

from werkzeug.exceptions import HTTPException


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'role_id'):
        identity.provides.add(RoleNeed(current_user.role.code))

@app.errorhandler(403)
def handle_403(e):
    template = '403.html'
    return render_template(template)



""" Index """
@app.route('/')
@login_required
def index():
    template = 'index.html'
    return render_template(template)

#---------------------------
##
## Login/Logout Routes
#---------------------------
""" Login """
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'GET':
        template = 'login.html'
        return render_template(template, form=login_form)


    if login_form.validate_on_submit() == False:
        for field, errors in login_form.errors.items():
            for error in errors:
                flash(error, "error")
        template = 'login.html'
        return render_template(template, form=login_form)


    if login_form.validate_on_submit() == True:
        username = login_form.username.data
        password = login_form.password.data

        try:
            user = User.query.filter_by(username=username).first()

            if user and User.verify_password(password, user.hashed_password):
                login_user(user)

                identity = Identity(user.id)
                identity_changed.send(app, identity=identity)

                flash(MSG["LOGIN_DONE"] + user.username, "success!")

                url  = url_for('index')
                # We need to check if next is safe_url or not
                # next = request.args.get('next')
                return redirect(url)

            else:
                flash(MSG["WRONG_CREDENTIALS"], "error")
                template = 'login.html'
                return render_template(template, form=login_form)

        except Exception as e:
            print e.message

            flash(MSG["UNEXPECTED_ERROR"], "error")
            template = 'login.html'
            return render_template(template, form=login_form)



""" Logout """
@app.route('/logout')
@login_required
def logout():
    logout_user()

    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(current_app, identity=AnonymousIdentity())

    flash(MSG["LOGOUT_DONE"], "success")
    url = url_for('login')
    return redirect(url)
