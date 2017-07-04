from flask            import current_app, request, session, url_for, redirect, \
                             render_template, flash, abort
from flask_principal  import Permission, RoleNeed, Identity, identity_changed, \
                             identity_loaded, UserNeed, AnonymousIdentity
from flask_login      import login_user, login_required, logout_user, current_user

from app import app, db, login_manager
from app.models import *
from app.forms import *
from app.constants import *
from app.permissions import *
from app.services import *

from datetime import datetime
from sqlalchemy import desc, or_, and_
import json, jsonify
import sqlalchemy



""" Get Users """
@app.route('/users', methods=['GET'])
@app.route('/users/page/<int:page>', methods=['GET'], endpoint='get_users_by_page')
@login_required
@administrators_permission.require(http_exception=403)
def get_users(page=1):
    search_string = request.args.get('str')

    if search_string:
        search_string = search_string.strip()

        users = User.query.filter(User.id != current_user.id) \
                          .filter(User.role_id != ROLES["root"][0]) \
                          .filter(User.role_id != current_user.role_id) \
                          .filter(User.firstname.like(search_string + "%")) \
                          .order_by(desc("updated_at")) \
                          .paginate(page, PER_PAGE["USERS"], False)

    else:
        users = User.query.filter(User.id != current_user.id) \
                          .filter(User.role_id != ROLES["root"][0]) \
                          .filter(User.role_id != current_user.role_id) \
                          .order_by(desc("updated_at")) \
                          .paginate(page, PER_PAGE["USERS"], False)

    template = 'users.html'
    response = render_template(template, users=users, page=page)

    return response



""" Add User """
@app.route('/users/new', methods=['GET', 'POST'])
@login_required
@administrators_permission.require(http_exception=403)
def add_user():
    if current_user.role.name == "root":
        AddUserForm = AddUserFormForRoot

    elif current_user.role.name == "admin":
        AddUserForm = AddUserFormForAdmin


    if request.method == "GET":
        add_user_form = AddUserForm()

        template = 'add_user.html'
        response = render_template(template, add_user_form=add_user_form)


    add_user_form = AddUserForm(request.form)
    if add_user_form.validate_on_submit() == False:
        for field, errors in add_user_form.errors.items():
            for error in errors:
                flash(error, "error")

        template = 'add_user.html'
        response = render_template(template, add_user_form=add_user_form)

    else:
        user = User()
        add_user_form.populate_obj(user)
        password = add_user_form.password.data
        user.hash_password(password)

        try:
            db.session.add(user)
            db.session.commit()

            flash(MSG["USER_PROFILE_CREATE_DONE"], "success")

            url = url_for('get_users')
            response = redirect(url)

        except sqlalchemy.exc.IntegrityError as e:
            print e.message
            db.session.rollback()

            flash(MSG["DUPLICATE_USER"], "error")

            template = 'add_user.html'
            response = render_template(template, add_user_form=add_user_form)

        except sqlalchemy.exc.DatabaseError as e:
            print e.message
            db.session.rollback()

            flash(MSG["OPERATION_FAILED"], "error")

            template = 'add_user.html'
            response = render_template(template, add_user_form=add_user_form)

    return response



""" Edit User """
@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@administrators_permission.require(http_exception=403)
def edit_user(user_id=None):
    if (user_id == current_user.id):
        url = url_for('edit_account_settings')
        return redirect(url)


    user = User.query.get(user_id)

    if not user:
        abot(404)


    if current_user.role.name == "root":
        EditUserForm = EditUserFormForRoot

    elif current_user.role.name == "admin":
        EditUserForm = EditUserFormForAdmin

    edit_user_form = EditUserForm(obj=user)

    if request.method == 'GET':
        template = 'edit_user.html'
        response =  render_template(template,
                               edit_user_form=edit_user_form,
                               change_user_password_form=ChangeUserPasswordForm(),
                               user_id=user.id)


    if "cancel" in request.form:
        url = url_for('get_users')
        response = redirect(url)


    elif 'update_profile' in request.form:
        edit_user_form = EditUserForm()


        if edit_user_form.validate_on_submit() == False:
            for field, errors in edit_user_form.errors.items():
                for error in errors:
                    flash(error, "error")


            template = "edit_user.html"
            response = render_template(template,
                            edit_user_form=edit_user_form,
                            change_user_password_form=ChangeUserPasswordForm(),
                            user_id=user.id)


        else:
            edit_user_form.populate_obj(user)
            user.updated_at = datetime.now()

            try:
                db.session.add(user)
                db.session.commit()

                flash(MSG["USER_PROFILE_EDIT_DONE"], "success")

                url = url_for('edit_user', user_id=user_id)
                response = redirect(url)

            except sqlalchemy.exc.IntegrityError as e:
                print e.message
                db.session.rollback()

                flash(MSG["USERNAME_IS_NOT_AVAILABLE"], "error")

                template = "edit_user.html"
                response = render_template(template,
                                edit_user_form=edit_user_form,
                                change_user_password_form=ChangeUserPasswordForm(),
                                user_id=user.id)

            except sqlalchemy.exc.DatabaseError as e:
                print e.message
                db.session.rollback()

                flash(MSG["OPERATION_FAILED"], "error")

                template = "edit_user.html"
                response = render_template(template,
                                edit_user_form=edit_user_form,
                                change_user_password_form=ChangeUserPasswordForm(),
                                user_id=user.id)


    elif "change_password" in request.form:
        user = User.query.get(user_id)
        edit_user_form = EditUserForm(formdata=None, obj=user)

        change_user_password_form = ChangeUserPasswordForm()

        if change_user_password_form.validate_on_submit() == False:
            for field, errors in change_user_password_form.errors.items():
                for error in errors:
                    flash(error, "error")

            template = "edit_user.html"
            response = render_template(template,
                            edit_user_form=edit_user_form,
                            change_user_password_form=ChangeUserPasswordForm(),
                            user_id=user.id)

        else:
            password = change_user_password_form.new_password.data
            user.hash_password(password)
            user.updated_at = datetime.now()

            try:
                db.session.add(user)
                db.session.commit()

                flash(MSG["USER_PASSWORD_CHANGE_DONE"], "success")

                url = url_for('edit_user', user_id=user.id)
                response = redirect(url)

            except sqlalchemy.exc.DatabaseError as e:
                print e.message
                db.session.rollback()

                flash(MSG["OPERATION_FAILED"], "error")


                template = "edit_user.html"
                response = render_template(template,
                                edit_user_form=edit_user_form,
                                change_user_password_form=ChangeUserPasswordForm(),
                                user_id=user.id)

    return response

""" Edit Account Settings """
@app.route('/account_settings/', methods=['GET', 'POST'])
@login_required
def edit_account_settings():
    user = current_user

    if request.method == 'GET':
        template = 'edit_account_settings.html'
        response = render_template(template,
                               edit_account_form=EditAccountForm(obj=user),
                               change_account_password_form=ChangeAccountPasswordForm(),
                               user_id=user.id)


    if "cancel" in request.form:
        url = url_for('index')
        response = redirect(url)


    elif 'update_profile' in request.form:
        edit_account_form = EditAccountForm(request.form)

        if edit_account_form.validate_on_submit() == False:
            for field, errors in edit_account_form.errors.items():
                for error in errors:
                    flash(error, "error")

            template = 'edit_account_settings.html'
            response = render_template(template,
                                    edit_account_form=edit_account_form,
                                    change_account_password_form=ChangeAccountPasswordForm(),
                                    user_id=user.id)

        else:
            edit_account_form.populate_obj(user)
            user.updated_at = datetime.now()

            try:
                db.session.add(user)
                db.session.commit()

                flash(MSG["USER_PROFILE_EDIT_DONE"], "success")

                url = url_for('edit_account_settings')
                response = redirect(url)

            except sqlalchemy.exc.IntegrityError as e:
                print e.message
                db.session.rollback()

                flash(MSG["USERNAME_IS_NOT_AVAILABLE"], "error")

                template = 'edit_account_settings.html'
                response = render_template(template,
                                        edit_account_form=edit_account_form,
                                        change_account_password_form=ChangeAccountPasswordForm(),
                                        user_id=user.id)

            except sqlalchemy.exc.DatabaseError as e:
                print e.message
                db.session.rollback()

                flash(MSG["OPERATION_FAILED"], "error")


                template = 'edit_account_settings.html'
                response = render_template(template,
                                        edit_account_form=edit_account_form,
                                        change_account_password_form=ChangeAccountPasswordForm(),
                                        user_id=user.id)

    elif "change_password" in request.form:
        user = current_user

        edit_account_form = EditAccountForm(formdata=None, obj=user)
        change_account_password_form = ChangeAccountPasswordForm(request.form)

        if change_account_password_form.validate_on_submit() == False:
            for field, errors in change_account_password_form.errors.items():
                for error in errors:
                    flash(error, "error")

            template = "edit_account_settings.html"
            response = render_template(template,
                            edit_account_form=edit_account_form,
                            change_account_password_form=ChangeAccountPasswordForm(),
                            user_id=user.id)


        else:
            old_password = change_account_password_form.old_password.data

            if user.verify_password(old_password, user.hashed_password) == False:
                flash(MSG["WRONG_OLD_PASSWORD"], "error")

                print 'yes'

                template = "edit_account_settings.html"
                response = render_template(template,
                                edit_account_form=edit_account_form,
                                change_account_password_form=ChangeAccountPasswordForm(),
                                user_id=user.id)

            else:
                new_password = change_account_password_form.new_password.data
                user.hash_password(new_password)
                user.updated_at = datetime.now()

                try:
                    db.session.add(user)
                    db.session.commit()

                    flash(MSG["USER_PASSWORD_CHANGE_DONE"], "success")

                    url = url_for('edit_account_settings')
                    response = redirect(url)

                except sqlalchemy.exc.DatabaseError as e:
                    print e.message
                    db.session.rollback()

                    flash(MSG["OPERATION_FAILED"], "error")

                    template = "edit_account_settings.html"
                    response = render_template(template,
                                    edit_account_form=edit_account_form,
                                    change_account_password_form=ChangeAccountPasswordForm(),
                                    user_id=user.id)

    return response


""" Delete User """
@app.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@administrators_permission.require(http_exception=403)
def delete_user(user_id=None):
    user = User.query.get(user_id)
    messages_list = {}

    if not user:
        abort(404)


    if user.role.name == current_user.role.name:
        flash_message = (MSG["USER_PROFILE_DELETE_DENIED"], "error")

        flash(*flash_message)
        url = url_for("get_users")
        response = redirect(url)


    else:
        try:
            db.session.delete(user)
            db.session.commit()

            flash_message = (MSG["USER_PROFILE_DELETE_DONE"], "success")

            flash(*flash_message)
            url = url_for("get_users")
            response = redirect(url)

        except sqlalchemy.exc.DatabaseError as e:
            print e.message
            db.session.rollback()

            flash_message = (MSG["OPERATION_FAILED"], "error")

            flash(*flash_message)
            url = url_for("get_users")
            response = redirect(url)

    return response
