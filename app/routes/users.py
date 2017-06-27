from flask            import current_app, request, session, url_for, redirect, \
                             render_template, flash
from flask_principal  import Permission, RoleNeed, Identity, identity_changed, \
                             identity_loaded, UserNeed, AnonymousIdentity
from flask_login      import login_user, login_required, logout_user, current_user

from app import app, db, login_manager
from app.models import *
from app.forms import *
from app.constants import MSG

from datetime import datetime
from sqlalchemy import desc, or_, and_
import json, jsonify


# Needs - Roles
be_superuser            = RoleNeed('superuser')
be_users_admin          = RoleNeed('users_admin')
be_investigation_doctor = RoleNeed('investigation_doctor')
be_registration_officer = RoleNeed('registration_officer')

# Permissions
admins_permission               = Permission(be_users_admin, be_superuser)
investigation_doctor_permission = Permission(be_investigation_doctor)
registration_officer_permission = Permission(be_registration_officer)



""" Get Users """
@app.route('/users', methods=['GET'])
@login_required
@admins_permission.require(http_exception=403)
def get_users():
    users = User.query.filter(or_(User.role_id.notin_([5]),
                                  User.role_id.is_(None))) \
                      .filter(User.id != current_user.id) \
                      .order_by(desc("updated_at")) \
                      .all()

    tempate = 'users.html'
    return render_template(tempate, users=users, users_is_active="active")



""" Add User """
@app.route('/users/new', methods=['GET', 'POST'])
@login_required
@admins_permission.require(http_exception=403)
def add_user():
    if request.method == "GET":
        add_user_form = AddUserForm()

        template = 'add_user.html'
        return render_template(template, add_user_form=add_user_form)

    add_user_form = AddUserForm(request.form)
    if add_user_form.validate_on_submit() == False:
        for field, errors in add_user_form.errors.items():
            for error in errors:
                flash(error, "error")

        template = 'add_user.html'
        return render_template(template, add_user_form=add_user_form)

    else:
        user = User()
        add_user_form.populate_obj(user)

        password = add_user_form.password.data
        user.hash_password(password)

        if db_update_or_insert_user(user) == False:
            flash(MSG["OPERATION_FAILED"], "error")

            template = 'add_user.html'
            return render_template(template, add_user_form=add_user_form)

        else:
            flash(MSG["USER_PROFILE_CREATED"], "success")

            url = url_for('get_users')
            return redirect(url)



""" Edit User """
@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admins_permission.require(http_exception=403)
def edit_user(user_id=None):
    if (user_id == current_user.id):
        url = url_for('edit_account_settings')
        return redirect(url)

    user = User.query.get(user_id)

    if request.method == 'GET':
        tempate = 'edit_user.html'
        return render_template(tempate,
                               edit_user_form=EditUserForm(obj=user),
                               change_user_password_form=ChangeUserPasswordForm(),
                               user_id=user.id)


    if "cancel" in request.form:
        url = url_for('get_users')
        return redirect(url)


    if 'update_profile' in request.form:
        edit_user_form = EditUserForm(request.form)
        change_user_password_form = ChangeUserPasswordForm()

        if edit_user_form.validate_on_submit() == False:
            for field, errors in edit_user_form.errors.items():
                for error in errors:
                    flash(error, "error")

            template = 'edit_user.html'
            return render_template(template,
                                    edit_user_form=edit_user_form,
                                    change_user_password_form=change_user_password_form,
                                    user_id=user.id)

        else:
            edit_user_form.populate_obj(user)

            if db_update_or_insert_user(user) == False:
                flash(MSG['OPERATION_FAILED'], 'error')

                template = 'edit_user.html'
                return render_template(template,
                                        edit_user_form=edit_user_form,
                                        change_user_password_form=change_user_password_form,
                                        user_id=user.id)

            else:
                flash(MSG["USER_PROFILE_EDIT_DONE"], "success")

                url = url_for('edit_user', user_id=user.id)
                return redirect(url)


    if "change_password" in request.form:
        user = User.query.get(user_id)

        change_user_password_form = ChangeUserPasswordForm(request.form)

        if change_user_password_form.validate_on_submit() == False:
            for field, errors in change_user_password_form.errors.items():
                for error in errors:
                    flash(error, "error")

            change_user_password_form = ChangeUserPasswordForm()
            edit_user_form = EditUserForm(obj=user)

            template = "edit_user.html"
            return render_template(template,
                            edit_user_form=edit_user_form,
                            change_user_password_form=change_user_password_form,
                            user_id=user.id)

        else:
            password = change_user_password_form.new_password.data
            user.hash_password(password)


            if db_update_or_insert_user(user) == False:
                change_user_password_form = ChangeUserPasswordForm()
                edit_user_form = EditUserForm(obj=user)

                flash(MSG["OPERATION_FAILED"], "error")

                template = "edit_user.html"
                return render_template(template,
                                edit_user_form=edit_user_form,
                                change_user_password_form=change_user_password_form,
                                user_id=user.id)

            else:
                flash(MSG["USER_PASSWORD_CHANGE_DONE"], "success")

                url = url_for("edit_user", user_id=user.id)
                return redirect(url)



""" User Account Settings """
@app.route('/account_settings/', methods=['GET', 'POST'])
@login_required
def edit_account_settings():
    user = current_user

    if request.method == 'GET':
        tempate = 'edit_account_settings.html'
        return render_template(tempate,
                               edit_account_form=EditAccountForm(obj=user),
                               change_account_password_form=ChangeAccountPasswordForm(),
                               user_id=user.id)


    if "cancel" in request.form:
        url = url_for('index')
        return redirect(url)


    if 'update_profile' in request.form:
        edit_account_form = EditAccountForm(request.form)
        change_account_password_form = ChangeAccountPasswordForm()

        if edit_account_form.validate_on_submit() == False:
            for field, errors in edit_account_form.errors.items():
                for error in errors:
                    flash(error, "error")

            template = 'edit_account_settings.html'
            return render_template(template,
                                    edit_account_form=edit_account_form,
                                    change_account_password_form=change_account_password_form,
                                    user_id=user.id)

        else:
            edit_account_form.populate_obj(user)

            if db_update_or_insert_user(user) == False:
                flash(MSG['OPERATION_FAILED'], 'error')

                template = 'edit_account_settings.html'
                return render_template(template,
                                        edit_account_form=edit_account_form,
                                        change_account_password_form=change_account_password_form,
                                        user_id=user.id)

            else:
                flash(MSG["USER_PROFILE_EDIT_DONE"], "success")

                url = url_for('edit_account_settings', user_id=user.id)
                return redirect(url)


    if "change_password" in request.form:
        user = current_user

        change_account_password_form = ChangeAccountPasswordForm(request.form)

        if change_account_password_form.validate_on_submit() == False:
            for field, errors in change_account_password_form.errors.items():
                for error in errors:
                    flash(error, "error")

            change_account_password_form = ChangeAccountPasswordForm()
            edit_account_form = EditAccountForm(obj=user)

            template = "edit_account_settings.html"
            return render_template(template,
                            edit_account_form=edit_account_form,
                            change_account_password_form=change_account_password_form,
                            user_id=user.id)

        else:
            change_account_password_form = ChangeAccountPasswordForm()
            edit_account_form = EditAccountForm(obj=user)

            old_password = change_account_password_form.old_password.data
            if user.verify_password(old_password, user.hashed_password) == False:
                flash(MSG["WRONG_OLD_PASSWORD"], "error")

                template = "edit_account_settings.html"
                return render_template(template,
                                edit_account_form=edit_account_form,
                                change_account_password_form=change_account_password_form,
                                user_id=user.id)

            new_password = change_account_password_form.new_password.data
            user.hash_password(new_password)

            if db_update_or_insert_user(user) == False:
                flash(MSG["OPERATION_FAILED"], "error")

                template = "edit_account_settings.html"
                return render_template(template,
                                edit_account_form=edit_account_form,
                                change_account_password_form=change_account_password_form,
                                user_id=user.id)

            else:
                flash(MSG["USER_PASSWORD_CHANGE_DONE"], "success")

                url = url_for("edit_account_settings", user_id=user.id)
                return redirect(url)



""" Delete User """
@app.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admins_permission.require(http_exception=403)
def delete_user(user_id=None):
    print user_id
    user = User.query.get(user_id)
    messages_list = {}

    print user.get_role_name()
    if user.role_id == 1 or user.role_id == 5:
        messages_list["error"] = MSG["USER_DELETE_DENIED"]

    elif db_delete_user(user) == False:
        messages_list["error"] = MSG["OPERATION_FAILED"]

    else:
        messages_list["success"] = MSG["USER_PROFILE_DELETE_DONE"]

    return json.dumps(messages_list)


def db_update_or_insert_user(user):
    user.updated_at = datetime.now()

    if user.role_id == '':
        user.role_id = None

    try:
        db.session.add(user)
        db.session.commit()

        return True

    except Exception as e:
        print e.message
        return False

def db_delete_user(user):
    try:
        db.session.delete(user)
        db.session.commit()

        return True

    except Exception as e:
        print e.message
        return False
