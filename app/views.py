from flask import request, session, url_for, redirect, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import desc

from app import app, db
from app.models import *
from app.constants import Enums
from app.forms import *

import json, jsonify


""" User: Index """
@app.route('/')
@login_required
def index():
    template = 'index.html'
    return render_template(template)


""" User: Register """
@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form);

    if request.method == 'GET':
        template = 'register.html'
        return render_template(template, form=register_form)


    if register_form.validate_on_submit() == False:
        for field, errors in register_form.errors.items():
            for error in errors:
                flash(error, "error")

        template = 'register.html'
        return render_template(template, form=register_form)


    if register_form.validate_on_submit() == True:
        password  = register_form.password.data

        try:
            user = User()
            user.hash_password(password)

            register_form.populate_obj(user)

            db.session.add(user)
            db.session.commit()

            flash(Enums["REGISTERATION_DONE"], "success")
            url = url_for('login')
            return redirect(url)

        except sqlalchemy.exc.IntegrityError as e:
            print e.message

            flash(Enums["DUPLICATE_USER"], "error")
            template = 'register.html'
            return render_template(template, form=register_form)

        except Exception as e:
            print e.message

            flash(Enums["UNEXPECTED_ERROR"], "error")
            template = 'register.html'
            return render_template(template, form=register_form)


""" User: Login """
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
                flash(Enums["LOGIN_DONE"] + user.username, "success")

                # We need to check if next is safe_url or not
                # print request.args.get('next')
                # next = request.args.get('next')
                url = url_for('index')
                return redirect(url)

            else:
                flash(Enums["WRONG_CREDENTIALS"], "error")
                template = 'login.html'
                return render_template(template, form=login_form)

        except Exception as e:
            print e.message

            flash(Enums["UNEXPECTED_ERROR"], "error")
            template = 'login.html'
            return render_template(template, form=login_form)


""" User: Logout """
@app.route('/logout')
@login_required
def logout():
    logout_user()

    flash(Enums["LOGOUT_DONE"], "success")
    url = url_for('login')
    return redirect(url)


""" Patient: New """
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
            flash(Enums["INVALID_PERSONAL_ID"], "error")
            template = "new_patient.html"
            return render_template(template, form=patient_form)


        patient = Patient.query.filter_by(personal_id=personal_id).first()
        if (patient):
            flash(Enums["DUPLICATE_PATIENT_ID"] % patient_form.personal_id.data, "error")
            template = "new_patient.html"
            return render_template(template, form=patient_form)

        try:
            patient = Patient()
            patient_form.populate_obj(patient)

            db.session.add(patient)
            db.session.commit()

            flash(Enums["PATIENT_ADDED"], "success")
            url = url_for('patient_analyzes', personal_id=patient.personal_id)
            return redirect(url)

        except:
            flash(Enums["UNEXPECTED_ERROR"], "error")
            template = "new_patient.html"
            return render_template(template, form=patient_form)



""" Patient: Edit Profile """
@app.route('/patient/profile/<string:personal_id>', methods=['GET', 'POST'])
@login_required
def edit_patient_profile(personal_id=None):
    patient = Patient.query.filter_by(personal_id=personal_id).first()

    if not patient:
        flash(Enums["NO_SUCH_PATIENT"], "error")
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

            flash(Enums["PATIENT_PROFILE_UPDATE_DONE"], "success")
            url = url_for('patient_analyzes', personal_id=patient.personal_id)
            return redirect(url)

        except Exception as e:
            print e.message
            flash(Enums["UNEXPECTED_ERROR"], "error")
            template = "patient_profile.html"
            return render_template(template, form=patient_form)



""" Patient: Delete """
@app.route('/patient/delete/personal_id/<string:personal_id>', methods=['GET'])
@login_required
def delete_patient_profile(personal_id=None):
    patient = Patient.query.filter_by(personal_id=personal_id).first()

    if (not patient):
        flash(Enums["NO_SUCH_PATIENT"], "error")
        url = url_for('index')
        return redirect(url)

    try:
        db.session.delete(patient)
        db.session.commit()

        flash(Enums["PATIENT_PROFILE_DELET_DONE"], 'success')
        url = url_for('index')
        return redirect(url)
    except Exception as e:
        print e.message
        flash(Enums["UNEXPECTED_ERROR"], "error")
        url = url_for('index')
        return redirect(url)



""" Patient: List of Patients """
@app.route('/patient')
@login_required
def list_of_patients():
    if request.args.get('json') == "True":
        patients = []

        patients_list = Patient.query.order_by(desc("updated_at")).all();
        for patient in patients_list:
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

    print request.args.get("json")

    if not patient:
        flash(Enums["NO_SUCH_PATIENT"], "error")
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



@app.route('/analysis/cbc_analysis/personal_id/<string:personal_id>', methods=['POST'])
@login_required
def add_cbc_analysis(personal_id=None):
    print request.args
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
        messages_list["success"] = []

        try:
            db.session.add(cbc_analysis_model)
            db.session.commit()

            messages_list["success"].append( Enums["CBC_ADD_DONE"] )
            return json.dumps(messages_list)

        except Exception as e:
            messages_list["error"] = []

            messages_list.append(Enums["UNEXPECTED_ERROR"])
            return json.dumps(messages_list)
