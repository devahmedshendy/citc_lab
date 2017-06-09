from flask import request, session, url_for, redirect, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from flask_sqlalchemy import sqlalchemy

from app import app, db
from app.models import User, Patient
from app.constants import Enums
from app.forms import LoginForm, RegisterForm, PatientForm, CBCAnalysisForm

import json, jsonify


""" User: Index """
@app.route('/')
@login_required
def index():
    return render_template('index.html')


""" User: Register """
@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form);

    if request.method == 'GET':
        return render_template('register.html', form=register_form)


    if register_form.validate_on_submit() == False:
        for field, errors in register_form.errors.items():
            for error in errors:
                flash(error, "error")
        return render_template('register.html', form=register_form)


    if register_form.validate_on_submit() == True:
        password  = register_form.password.data

        try:
            user = User()
            user.hash_password(password)

            register_form.populate_obj(user)

            db.session.add(user)
            db.session.commit()

            flash(Enums["REGISTERATION_DONE"], "success")
            return redirect( url_for('login') )

        except sqlalchemy.exc.IntegrityError as e:
            print e.message

            flash(Enums["DUPLICATE_USER"], "error")
            return render_template('register.html', form=register_form)

        except Exception as e:
            print e.message

            flash(Enums["UNEXPECTED_ERROR"], "error")
            return render_template('register.html', form=register_form)


""" User: Login """
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'GET':
        return render_template('login.html', form=login_form)


    if login_form.validate_on_submit() == False:
        for field, errors in login_form.errors.items():
            for error in errors:
                flash(error, "error")
        return render_template('login.html', form=login_form)


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
                return redirect(url_for('index'))

            else:
                flash(Enums["WRONG_CREDENTIALS"], "error")
                return render_template('login.html', form=login_form)

        except Exception as e:
            print e.message

            flash(Enums["UNEXPECTED_ERROR"], "error")
            return render_template('login.html', form=login_form)


""" User: Logout """
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(Enums["LOGOUT_DONE"], "success")
    return redirect(url_for('login'))


""" Patient: New """
@app.route('/patient/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    patient_form = PatientForm(request.form)

    if request.method == 'GET':
        return render_template("new_patient.html", form=patient_form)


    if patient_form.validate_on_submit() == False:
            for field, errors in patient_form.errors.items():
                for error in errors:
                    flash(error, "error")

            return render_template("new_patient.html", form=patient_form)


    if patient_form.validate_on_submit() == True:
        personal_id = patient_form.personal_id.data
        if (len(personal_id) != 14):
            flash(Enums["INVALID_PERSONAL_ID"], "error")
            return render_template("new_patient.html", form=patient_form)


        patient = Patient.query.filter_by(personal_id=personal_id).first()
        if (patient):
            print 'here'
            flash(Enums["DUPLICATE_PATIENT_ID"] % patient_form.personal_id.data, "error")
            return render_template("new_patient.html", form=patient_form)

        try:
            patient = Patient()
            patient_form.populate_obj(patient)

            db.session.add(patient)
            db.session.commit()

            print 'added'
            flash(Enums["PATIENT_ADDED"], "success")
            return redirect(url_for('patient_analyzes', personal_id=patient.personal_id))

        except:
            flash(Enums["UNEXPECTED_ERROR"], "error")
            return render_template("new_patient.html", form=patient_form)



""" Patient: Edit Profile """
@app.route('/patient/profile/<string:personal_id>', methods=['GET', 'POST'])
@login_required
def edit_patient_profile(personal_id=None):
    patient = Patient.query.filter_by(personal_id=personal_id).first()

    if not patient:
        flash(Enums["NO_SUCH_PATIENT"], "error")
        return redirect( url_for('index') )

    patient_form = PatientForm(obj=patient)

    if request.method == 'GET':
        return render_template("patient_profile.html", form=patient_form)

    if patient_form.validate_on_submit() == False:
        for field, errors in patient_form.errors.items():
            for error in errors:
                flash(error, "error")
        return render_template('patient_profile.html', form=patient_form)

    if patient_form.validate_on_submit() == True:

        try:
            patient_form.populate_obj(patient)
            patient.updated_at = datetime.now()

            db.session.add(patient)
            db.session.commit()

            flash(Enums["PATIENT_PROFILE_UPDATE_DONE"], "success")
            return redirect(url_for('patient_analyzes', personal_id=patient_form.personal_id.data))

        except:
            flash(Enums["UNEXPECTED_ERROR"], "error")
            return render_template("new_patient.html", form=patient_form)



""" Patient: Delete """
@app.route('/patient/delete/personal_id/<string:personal_id>', methods=['GET'])
@login_required
def delete_patient_profile(personal_id=None):
    patient = Patient.query.filter_by(personal_id=personal_id).first()

    if (not patient):
        flash(Enums["NO_SUCH_PATIENT"], "error")
        return redirect( url_for('index') )

    try:
        db.session.delete(patient)
        db.session.commit()

        flash(Enums["PATIENT_PROFILE_DELET_DONE"], 'success')
        return redirect( url_for('index') )
    except Exception as e:
        print e.message
        flash(Enums["UNEXPECTED_ERROR"], "error")
        return redirect( url_for('index') )



""" Patient: List of Patients """
@app.route('/patient')
@login_required
def list_of_patients():
    if request.args.get('json') == "list_of_patients":
        patients = []

        patients_list = Patient.query.limit(10).all();
        for patient in patients_list:
            patients.append({
                'personal_id'   : patient.personal_id,
                'name'          : patient.name,
                'updated_at'    : patient.updated_at.strftime("%b %d, %Y - %I:%M %p")
            })

        return json.dumps(patients)


# """ Display Patient's Analysis """
# @app.route('/analysis')



""" Patient: Analyzes Profile """
@app.route('/analysis/personal_id/<string:personal_id>', methods=['GET', 'POST'])
@login_required
def patient_analyzes(personal_id=None):
    patient = Patient.query.filter_by(personal_id=personal_id).first()
    patient_form = PatientForm(obj=patient)
    cbc_analysis_form = CBCAnalysisForm(request.form)

    if not patient:
        flash(Enums["NO_SUCH_PATIENT"], "error")
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template('analysis_profile.html', form=cbc_analysis_form, patient_form=patient_form)

    if cbc_analysis_form.validate_on_submit() == False:
        for field, errors in cbc_analysis_form.errors.items():
            for error in errors:
                flash(error, "error")
        print 'cbc_analysis_form validate error'
        return render_template('analysis_profile.html', form=cbc_analysis_form, patient=patient, modalStatus='show')

    if cbc_analysis_form.validate_on_submit() == True:
        print 'cbc_analysis_form validate success'
        flash('cbc_analysis_form validate success', 'success')
        return render_template('analysis_profile.html', form=cbc_analysis_form, patient=patient)
