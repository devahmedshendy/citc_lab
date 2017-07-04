from flask            import current_app, request, session, url_for, redirect, \
                             render_template, flash, Markup, abort
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



""" Get Patients """
@app.route('/patients', methods=['GET'])
@app.route('/patients/page/<int:page>', methods=['GET'], endpoint='get_patients_by_page')
@login_required
def get_patients(page=1):
    search_string = request.args.get('str')

    if search_string:
        search_string = search_string.strip()

        try:
            int(search_string)

            patients = Patient.query.order_by(desc("updated_at")) \
                            .filter(Patient.personal_id.like(search_string + "%")) \
                            .paginate(page, PER_PAGE["PATIENTS"], False)

        except ValueError:
            patients = Patient.query.order_by(desc("updated_at")) \
                            .filter(Patient.name.like(search_string + "%")) \
                            .paginate(page, PER_PAGE["PATIENTS"], False)

    else:
        patients = Patient.query.order_by(desc("updated_at")) \
                    .paginate(page, PER_PAGE["PATIENTS"], False)

    template = 'patients.html'
    return render_template(template, patients=patients, page=page)



""" Add Patient """
@app.route('/patients/new', methods=['GET', 'POST'])
@login_required
@officer_permission.require(http_exception=403)
def add_patient():
    if request.method == "GET":
        add_patient_form = AddPatientForm()

        template = 'add_patient.html'
        return render_template(template, add_patient_form=add_patient_form)

    add_patient_form = AddPatientForm(request.form)
    if add_patient_form.validate_on_submit() == False:
        for field, errors in add_patient_form.errors.items():
            for error in errors:
                flash(error, "error")

    else:
        patient = Patient()
        add_patient_form.populate_obj(patient)

        try:
            db.session.add(patient)
            db.session.commit()

            flash_message = (MSG["PATIENT_PROFILE_CREATE_DONE"], "success")

            flash(*flash_message)
            url = url_for('get_patients')
            return redirect(url)


        except sqlalchemy.exc.IntegrityError as e:
            print e.message
            db.session.rollback()

            if "UNIQUE" in e.message or "Duplicate" in e.message:
                same_patient = patient_of_personal_id(patient.personal_id)

                patient_profile_link = "<a href='/patients/%s'>%s</a>" % (same_patient.id, same_patient.name)
                flash_message = (Markup( MSG["DUPLICATE_PERSONAL_ID"] % (patient_profile_link) ), "error")
                flash(*flash_message)

        except sqlalchemy.exc.DatabaseError as e:
            print e.message
            db.session.rollback()

            flash_message = (MSG["OPERATION_FAILED"], "error")
            flash(*flash_message)


    template = 'add_patient.html'
    return render_template(template, add_patient_form=add_patient_form)



""" Edit Patient """
@app.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@officer_permission.require(http_exception=403)
def edit_patient(patient_id=None):
    patient = get_patient(patient_id=patient_id)

    if not patient:
        abort(404)


    if request.method == 'GET':
        tempate = 'edit_patient.html'
        return render_template(tempate,
                               edit_patient_form=EditPatientForm(obj=patient),
                               patient_id=patient.id)


    if "cancel" in request.form:
        url = url_for('get_patients')
        return redirect(url)


    if 'update_profile' in request.form:
        edit_patient_form = EditPatientForm(request.form)

        if edit_patient_form.validate_on_submit() == False:
            for field, errors in edit_patient_form.errors.items():
                for error in errors:
                    flash(error, "error")

        else:
            edit_patient_form.populate_obj(patient)

            try:
                print patient.personal_id
                db.session.add(patient)
                db.session.commit()

                flash_message = (MSG["PATIENT_PROFILE_EDIT_DONE"], "success")
                flash(*flash_message)

            except sqlalchemy.exc.IntegrityError as e:
                print e.message
                db.session.rollback()

                if "UNIQUE" in e.message or "Duplicate" in e.message:
                    same_patient = get_patient(personal_id=edit_patient_form.personal_id.data)

                    patient_profile_link = "<a href='/patients/%s'>%s</a>" % (same_patient.id, same_patient.name)

                    flash_message = (Markup( MSG["DUPLICATE_PERSONAL_ID"] % (patient_profile_link) ), "error")
                    flash(*flash_message)


            except sqlalchemy.exc.DatabaseError as e:
                print e.message
                db.session.rollback()

                flash_message = (MSG["OPERATION_FAILED"], "error")
                flash(*flash_message)

            template = 'edit_patient.html'
            return render_template(template,
                                    edit_patient_form=edit_patient_form,
                                    patient_id=patient.id)



""" Display Patient Profile """
@app.route('/patients/<int:patient_id>', methods=['GET'])
@login_required
def get_patient_personal_profile(patient_id=None):
    patient = get_patient(patient_id=patient_id)

    if not patient:
        abort(404)

    edit_patient_form = EditPatientForm(obj=patient)

    tempate = 'patient_personal_profile.html'
    return render_template(tempate, edit_patient_form=edit_patient_form)



""" Get Patient Medical Profile """
@app.route('/patients/<int:patient_id>/medical_profile', methods=['GET'], endpoint="medical_profile")
@app.route('/patients/<int:patient_id>/analyzes', methods=['GET'])
@login_required
def get_patient_analyzes(patient_id=None):
    patient = get_patient(patient_id=patient_id)

    if not patient:
        abort(404)

    edit_patient_form = EditPatientForm(obj=patient)
    add_cbc_form      = AddCBCForm()

    if request.method == "GET" and request.args.get("json") == None:
        template = 'patient_medical_profile.html'
        return render_template(template, edit_patient_form=edit_patient_form,
                                         add_cbc_form=add_cbc_form,
                                         patient_id=patient.id)

    if request.method == "GET" and request.args.get("json") == "True":
        cbc_analysis_list = []

        analyzes = get_all_analyzes_of_patient(patient.id)

        for cbc_analysis in analyzes:
            cbc_analysis_list.append(cbc_analysis.serialize())

        return json.dumps(cbc_analysis_list)



""" Delete Patient """
@app.route('/patients/delete/<int:patient_id>', methods=['POST'])
@login_required
@officer_permission.require(http_exception=403)
def delete_patient(patient_id=None):
    patient = get_patient(patient_id)

    if not patient:
        abort(404)

    try:
        db.session.delete(patient)
        db.session.commit()

        flash_message = (MSG["PATIENT_PROFILE_DELETE_DONE"], "success")

    except sqlalchemy.exc.DatabaseError as e:
        print e.message
        db.session.rollback()

        flash_message = (MSG["OPERATION_FAILED"], "error")

    flash(*flash_message)
    url = url_for('get_patients')
    return redirect(url)
