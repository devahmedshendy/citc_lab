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


# # Needs
# be_admin    = RoleNeed('admin')
# be_doctor   = RoleNeed('doctor')
# be_officer  = RoleNeed('officer')
#
# # Permissions
# admin_permission   = Permission(be_admin)
# doctor_permission  = Permission(be_doctor)
# officer_permission = Permission(be_officer)
#
# app_needs = [be_admin, be_doctor, be_officer]
# app_permissions = [admin_permission, doctor_permission, officer_permission]


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'role_id'):
        identity.provides.add(RoleNeed(current_user.get_role_name()))

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



# """ User: Register """
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     register_form = RegisterForm(request.form);
#
#     if request.method == 'GET':
#         template = 'register.html'
#         return render_template(template, form=register_form)
#
#
#     if register_form.validate_on_submit() == False:
#         for field, errors in register_form.errors.items():
#             for error in errors:
#                 flash(error, "error")
#
#         template = 'register.html'
#         return render_template(template, form=register_form)
#
#
#     if register_form.validate_on_submit() == True:
#         password  = register_form.password.data
#
#         try:
#             user = User()
#             user.hash_password(password)
#
#             register_form.populate_obj(user)
#
#             db.session.add(user)
#             db.session.commit()
#
#             flash(MSG["REGISTERATION_DONE"], "success")
#             url = url_for('login')
#             return redirect(url)
#
#         except sqlalchemy.exc.IntegrityError as e:
#             print e.message
#
#             flash(MSG["DUPLICATE_USER"], "error")
#             template = 'register.html'
#             return render_template(template, form=register_form)
#
#         except Exception as e:
#             print e.message
#
#             flash(MSG["UNEXPECTED_ERROR"], "error")
#             template = 'register.html'
#             return render_template(template, form=register_form)

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
                user.authenticated = True

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

#---------------------------
##
## User Routes
#---------------------------
# """ Get Users """
# @app.route('/users', methods=['GET'])
# @admin_permission.require(http_exception=403)
# @login_required
# def get_users():
#     return '/users'
#
#
#
# """ Add User """
# @app.route('/users/new', methods=['GET', 'POST'])
# @admin_permission.require(http_exception=403)
# @login_required
# def add_user():
#     return '/users/new'
#
#
#
# """ Add User """
# @app.route('/users/edit', methods=['GET', 'POST'])
# @admin_permission.require(http_exception=403)
# @login_required
# def edit_user():
#     return '/users/edit'

#---------------------------
##
## Patient Routes
#---------------------------
""" Patient: Add Patient Profile """
@app.route('/patient/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    patient_form = PatientForm(request.form)

    if request.method == 'GET':
        template = "new_patient.html"
        return render_template(template, form=patient_form)


    if patient_form.validate_on_submit() == False:
            for field, errors in patient_form.errors.items():
                for error in errors:
                    flash(error, "error")

            template = "new_patient.html"
            return render_template(template, form=patient_form)


    if patient_form.validate_on_submit() == True:
        personal_id = patient_form.personal_id.data

        if (len(personal_id) != 14):
            flash(MSG["INVALID_PERSONAL_ID"], "error")
            template = "new_patient.html"
            return render_template(template, form=patient_form)


        patient = Patient.query.filter_by(personal_id=personal_id).first()
        if (patient):
            flash(MSG["DUPLICATE_PATIENT_ID"] % patient_form.personal_id.data, "error")
            template = "new_patient.html"
            return render_template(template, form=patient_form)

        try:
            patient = Patient()
            patient_form.populate_obj(patient)

            db.session.add(patient)
            db.session.commit()

            flash(MSG["PATIENT_ADDED"], "success")
            url = url_for('patient_analyzes', personal_id=patient.personal_id)
            return redirect(url)

        except Exception as e:
            print e.message

            flash(MSG["UNEXPECTED_ERROR"], "error")
            template = "new_patient.html"
            return render_template(template, form=patient_form)



""" Patient: Edit Profile """
@app.route('/patient/profile/<string:personal_id>', methods=['GET', 'POST'])
@login_required
def edit_patient_profile(personal_id=None):
    patient = Patient.query.filter_by(personal_id=personal_id).first()

    if not patient:
        flash(MSG["NO_SUCH_PATIENT"], "error")
        url = url_for('index')
        return redirect(url)

    patient_form = PatientForm(obj=patient)

    if request.method == 'GET':
        template = "patient_profile.html"
        return render_template(template, form=patient_form)

    if patient_form.validate_on_submit() == False:
        for field, errors in patient_form.errors.items():
            for error in errors:
                flash(error, "error")

        template = 'patient_profile.html'
        return render_template(template, form=patient_form)


    if patient_form.validate_on_submit() == True:

        try:
            patient_form.populate_obj(patient)
            patient.updated_at = datetime.now()

            db.session.add(patient)
            db.session.commit()

            flash(MSG["PATIENT_PROFILE_UPDATE_DONE"], "success")
            url = url_for('patient_analyzes', personal_id=patient.personal_id)
            return redirect(url)

        except Exception as e:
            print e.message

            flash(MSG["UNEXPECTED_ERROR"], "error")
            template = "patient_profile.html"
            return render_template(template, form=patient_form)



""" Patient: Delete Profile """
@app.route('/patient/delete/personal_id/<string:personal_id>', methods=['GET'])
@login_required
def delete_patient_profile(personal_id=None):
    patient = Patient.query.filter_by(personal_id=personal_id).first()

    if (not patient):
        flash(MSG["NO_SUCH_PATIENT"], "error")
        url = url_for('index')
        return redirect(url)

    try:
        db.session.delete(patient)
        db.session.commit()

        flash(MSG["PATIENT_PROFILE_DELET_DONE"], 'success')
        url = url_for('index')
        return redirect(url)
    except Exception as e:
        print e.message

        flash(MSG["UNEXPECTED_ERROR"], "error")
        url = url_for('index')
        return redirect(url)



""" Patient: List of Patients """
@app.route('/patient/json', methods=["GET"])
@app.route('/patient/search/json', methods=["GET"])
@login_required
def list_of_patients():
    patients = []
    query_result = []

    startswith_string = request.args.get('startswith')

    if startswith_string == None:
        query_result = Patient.query.order_by(desc("updated_at")).all();

    elif len(startswith_string) > 0:
        query_result = Patient.query.filter(
                            Patient.personal_id.startswith(startswith_string)
                            ).order_by(desc("updated_at")).all();

    for patient in query_result:
        patients.append({
            'personal_id'   : patient.personal_id,
            'name'          : patient.name,
            'updated_at'    : patient.updated_at.strftime("%b %d, %Y - %I:%M %p")
        })

    return json.dumps(patients)



""" Patient: Analyzes Profile """
@app.route('/analysis/personal_id/<string:personal_id>', methods=['GET'])
@login_required
def patient_analyzes(personal_id=None):
    patient = Patient.query.filter_by(personal_id=personal_id).first()
    patient_form = PatientForm(obj=patient)
    cbc_analysis_form = CBCAnalysisForm(request.form)

    if not patient:
        flash(MSG["NO_SUCH_PATIENT"], "error")
        url = url_for("index")
        return redirect(url)


    if request.method == "GET" and request.args.get("json") == None:
        template = 'analysis_profile.html'
        return render_template(template, cbc_analysis_form=cbc_analysis_form,
                                    patient_form=patient_form)


    if request.method == "GET" and request.args.get("json") == "True":
        cbc_analysis_list = []

        query_result = CBCAnalysis.query.filter_by(patient_id=patient.id) \
                            .order_by(desc("updated_at")).all()
        for cbc_analysis in query_result:
            cbc_analysis_list.append(cbc_analysis.serialize())

        return json.dumps(cbc_analysis_list)



""" CBC: Add Analysis """
@app.route('/analysis/cbc_analysis/personal_id/<string:personal_id>', methods=['POST'])
@login_required
def add_cbc_analysis(personal_id=None):
    messages_list = {}

    cbc_submitted_data = request.get_json()

    patient = Patient.query.filter_by(personal_id=personal_id).first()

    cbc_analysis_model = CBCAnalysis(
                            cbc_submitted_data["WCB"],
                            cbc_submitted_data["HGB"],
                            cbc_submitted_data["MCV"],
                            cbc_submitted_data["MCH"],
                            1,
                            patient.id,
                            cbc_submitted_data["comment"])

    cbc_analysis_form = CBCAnalysisForm(obj=cbc_analysis_model)


    if cbc_analysis_form.validate() == False:
        messages_list["error"] = []

        for field, errors in cbc_analysis_form.errors.items():
            for error in errors:
                messages_list["error"].append(error)

        return json.dumps(messages_list)


    if cbc_analysis_form.validate() == True:
        try:
            db.session.add(cbc_analysis_model)
            db.session.commit()

            messages_list["success"] = MSG["CBC_ANALYSIS_ADD_DONE"]
            return json.dumps(messages_list)

        except Exception as e:
            print e.message
            messages_list["error"] = []

            messages_list.append(MSG["UNEXPECTED_ERROR"])
            return json.dumps(messages_list)


""" CBC: Delete Analysis """
@app.route('/analysis/cbc_analysis/personal_id/<string:personal_id>/cbc_id/<string:cbc_id>', methods=['GET'])
@login_required
def delete_cbc_analysis(personal_id=None, cbc_id=None):
    try:
        CBCAnalysis.query.filter_by(id=cbc_id).delete()
        # db.session.delete(cbc_analysis)
        db.session.commit()

        flash(MSG["CBC_ANALYSIS_DELETE_DONE"], 'success')
        url = url_for('patient_analyzes', personal_id=personal_id)
        return redirect(url)

    except Exception as e:
        print e.message

        flash(MSG["UNEXPECTED_ERROR"], "error")
        url = url_for('patient_analyzes', personal_id=personal_id)
        return redirect(url)


""" CBC: Edit Analysis """
@app.route('/analysis/personal_id/<string:personal_id>/cbc_id/<string:cbc_id>', methods=['POST'])
@login_required
def edit_cbc_profile(personal_id=None, cbc_id=None):
    messages_list = {}

    cbc_analysis = CBCAnalysis.query \
                        .join(Patient, Patient.id==CBCAnalysis.patient_id) \
                        .filter(CBCAnalysis.id == cbc_id) \
                        .first()


    if (not cbc_analysis):
        messages_list["error"] = []
        messages_list["error"].append(MSG["NO_SUCH_CBC_ANALYSIS"] )

        return json.dumps(messages_list)


    cbc_submitted_data = request.get_json()

    cbc_analysis_form = CBCAnalysisForm()

    cbc_analysis_form.comment.data = cbc_submitted_data["comment"]
    cbc_analysis_form.WCB.data = cbc_submitted_data["WCB"]
    cbc_analysis_form.HGB.data = cbc_submitted_data["HGB"]
    cbc_analysis_form.MCV.data = cbc_submitted_data["MCV"]
    cbc_analysis_form.MCH.data = cbc_submitted_data["MCH"]


    if cbc_analysis_form.validate_on_submit() == False:
        messages_list["error"] = []

        for field, errors in cbc_analysis_form.errors.items():
            for error in errors:
                messages_list["error"].append(error)

        return json.dumps(messages_list)


    if cbc_analysis_form.validate_on_submit() == True:
        cbc_analysis_form.populate_obj(cbc_analysis)

    try:
        db.session.add(cbc_analysis)
        db.session.commit()

        messages_list["success"] = MSG["CBC_ANALYSIS_EDIT_DONE"]

        return json.dumps(messages_list)

    except Exception as e:
        print e.message
        messages_list["error"] = []
        messages_list["error"].append(MSG["UNEXPECTED_ERROR"])

        return json.dumps(messages_list)



""" CBC: Print Analysis """
# This needs https://www.cairographics.org/download/ to be installed \
# in the server hosting this website.
@app.route('/analysis/personal_id/<string:personal_id>/cbc_id/<string:cbc_id>', methods=['GET'])
@login_required
def print_cbc_analysis(personal_id=None, cbc_id=None):
    messages_list = {}

    cbc_analysis = CBCAnalysis.query \
                        .join(Patient, Patient.id==CBCAnalysis.patient_id) \
                        .filter(CBCAnalysis.id == cbc_id) \
                        .add_columns(Patient.personal_id,
                                    Patient.name,
                                    Patient.age,
                                    Patient.gender,
                                    CBCAnalysis.id,
                                    CBCAnalysis.comment,
                                    CBCAnalysis.WCB,
                                    CBCAnalysis.HGB,
                                    CBCAnalysis.MCV,
                                    CBCAnalysis.MCH,
                                    CBCAnalysis.created_at,
                                    CBCAnalysis.updated_at).first()




    if (not cbc_analysis):
        messages_list["error"] = []
        messages_list["error"].append(MSG["NO_SUCH_CBC_ANALYSIS"] )

        return json.dumps(messages_list)



    template = 'cbc_analysis_pdf.html'
    html = render_template(template, cbc=cbc_analysis)
    return render_pdf(HTML(string=html))
