from flask import request, session, url_for, redirect, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from flask_sqlalchemy import sqlalchemy

from app import app, db
from app.models import User, Patient
from app.services import UserService
from app.constants import Enums

from forms import LoginForm, RegisterForm, PatientForm

import json, jsonify


""" Home """
@app.route('/')
@login_required
def index():
    return render_template('index.html')


""" Register """
@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form);

    if request.method == 'POST':
        if register_form.validate() == False:
            for field, errors in register_form.errors.items():
                for error in errors:
                    flash(error, "error")

        else:
            firstname = register_form.user_firstname.data.strip().title()
            lastname  = register_form.user_lastname.data.strip().title()
            username  = register_form.user_username.data.strip()
            password  = register_form.user_password.data.strip()

            user = User(firstname, lastname, username, password)

            try:
                db.session.add(user)
                db.session.commit()

                flash(Enums["REGISTERATION_DONE"], "success")
                return redirect('/login')

            except sqlalchemy.exc.IntegrityError as e:
                flash(Enums["DUPLICATE_USER"], "error")

            except:
                flash(Enums["UNEXPECTED_ERROR"], "error")

    return render_template('register.html', form=register_form)


""" Login """
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'POST':
        if login_form.validate() == False:
            for field, errors in login_form.errors.items():
                for error in errors:
                    flash(error, "error")
            return render_template('login.html', form=login_form)

        username = login_form.user_username.data
        password = login_form.user_password.data

        try:
            registered_user = User.query.filter_by(username=username).first()
            if registered_user and User.verify_password(password, registered_user.hashed_password):
                login_user(registered_user)
                registered_user.authenticated = True
                flash(Enums["LOGIN_DONE"] + registered_user.username, "success")

                # We need to check if next is safe_url or not
                # print request.args.get('next')
                # next = request.args.get('next')
                return redirect(url_for('index'))

            else:
                flash(Enums["WRONG_CREDENTIALS"], "error")

        except Exception as e:
            flash(Enums["UNEXPECTED_ERROR"], "error")
            print e.message

    return render_template('login.html', form=login_form)


""" Logout """
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(Enums["LOGOUT_DONE"], "success")
    return redirect(url_for('login'))


""" Adding New Patient """
@app.route('/patient/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    patient_form = PatientForm(request.form)

    if request.method == 'GET':
        return render_template("new_patient.html", form=patient_form)

    if request.method == 'POST':
        if patient_form.validate() == False:
            for field, errors in patient_form.errors.items():
                for error in errors:
                    flash(error, "error")

            return render_template("new_patient.html", form=patient_form)


        else:
            personal_id   = patient_form.patient_personal_id.data
            name          = patient_form.patient_name.data
            address       = patient_form.patient_address.data
            phone         = patient_form.patient_phone.data
            age           = patient_form.patient_age.data
            gender        = patient_form.patient_gender.data

            if (len(personal_id) != 14):
                flash(Enums["INVALID_PERSONAL_ID"], "error")

                return render_template("new_patient.html", form=patient_form)


            added_patient = Patient.query.filter_by(personal_id=personal_id).first()
            if (added_patient):
                flash(Enums["DUPLICATE_PATIENT_ID"] % patient_form.patient_personal_id.data, "error")

                return render_template("new_patient.html", form=patient_form)

            try:
                patient = Patient(personal_id, name, address, phone, age, gender)
                db.session.add(patient)
                db.session.commit()

                flash(Enums["PATIENT_ADDED"], "success")
                return redirect(url_for('edit_patient_profile', patient_personal_id=patient.personal_id))

            except:
                flash(Enums["UNEXPECTED_ERROR"], "error")
                return render_template("new_patient.html", form=patient_form)



""" Edit Patient Account Profile """
@app.route('/patient/profile/<string:patient_personal_id>', methods=['GET', 'POST'])
@login_required
def edit_patient_profile(patient_personal_id=None):
    patient = Patient.query.filter_by(personal_id=patient_personal_id).first()

    if not patient:
        flash(Enums["NO_SUCH_PATIENT"], "error")
        return redirect( url_for('index') )

    if request.method == 'GET':
        return render_template("patient_profile.html", patient=patient)

    if request.method == 'POST':
        patient.personal_id = request.form["patient_personal_id"]
        patient.name = request.form["patient_name"]
        patient.address = request.form["patient_address"]
        patient.phone = request.form["patient_phone"]
        patient.age = request.form["patient_age"]
        patient.gender = request.form["patient_gender"]
        patient.updated_at = datetime.now()

        db.session.commit()

        flash(Enums["PATIENT_PROFILE_UPDATED"], "success")
        return redirect(url_for('edit_patient_profile', patient_personal_id=patient.personal_id))



""" Get List of Patients """
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
                'address'       : patient.address,
                'phone'         : patient.phone,
                'age'           : patient.age,
                'gender'        : patient.gender,
                'updated_at'    : patient.updated_at.strftime("%Y-%m-%d")
            })

        return json.dumps(patients)
