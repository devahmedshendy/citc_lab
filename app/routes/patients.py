from flask            import current_app, request, session, url_for, redirect, \
                             render_template, flash
from flask_principal  import Permission, RoleNeed, Identity, identity_changed, \
                             identity_loaded, UserNeed, AnonymousIdentity
from flask_login      import login_user, login_required, logout_user, current_user

from app import app, db, login_manager
from app.models import *
from app.forms import *
from app.constants import *
from app.permissions import *

from datetime import datetime
from sqlalchemy import desc, or_, and_
import json, jsonify


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

        template = 'add_patient.html'
        return render_template(template, add_patient_form=add_patient_form)

    else:
        patient = Patient()
        add_patient_form.populate_obj(patient)

        if db_update_or_insert_patient(patient) == False:
            flash(MSG["OPERATION_FAILED"], "error")

            template = 'add_patient.html'
            return render_template(template, add_patient_form=add_patient_form)

        else:
            flash(MSG["USER_PROFILE_CREATED"], "success")

            url = url_for('get_patients')
            return redirect(url)



""" Edit Patient """
@app.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@officer_permission.require(http_exception=403)
def edit_patient(patient_id=None):
    patient = Patient.query.get(patient_id)

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

            template = 'edit_patient.html'
            return render_template(template,
                                    edit_patient_form=edit_patient_form,
                                    patient_id=patient.id)

        else:
            edit_patient_form.populate_obj(patient)

            if db_update_or_insert_patient(patient) == False:
                flash(MSG['OPERATION_FAILED'], 'error')

                template = 'edit_patient.html'
                return render_template(template,
                                        edit_patient_form=edit_patient_form,
                                        patient_id=patient.id)

            else:
                flash(MSG["USER_PROFILE_EDIT_DONE"], "success")

                url = url_for('edit_patient', patient_id=patient.id)
                return redirect(url)



""" Display Patient Profile """
@app.route('/patients/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def get_patient_personal_profile(patient_id=None):
    patient = Patient.query.get(patient_id)

    edit_patient_form = EditPatientForm(obj=patient)

    tempate = 'patient_personal_profile.html'
    return render_template(tempate, edit_patient_form=edit_patient_form)



""" Get Patient Medical Profile """
@app.route('/patients/<int:patient_id>/medical_profile', methods=['GET'], endpoint="medical_profile")
@app.route('/patients/<int:patient_id>/analyzes', methods=['GET'])
@login_required
def get_patient_analyzes(patient_id=None):
    patient = Patient.query.get(patient_id)

    if not patient:
        flash(MSG["NO_SUCH_PATIENT"], "error")
        url = url_for("index")
        return redirect(url)

    edit_patient_form = EditPatientForm(obj=patient)
    add_cbc_form      = AddCBCForm()

    if request.method == "GET" and request.args.get("json") == None:
        template = 'patient_medical_profile.html'
        return render_template(template, edit_patient_form=edit_patient_form,
                                         add_cbc_form=add_cbc_form,
                                         patient_id=patient.id)

    if request.method == "GET" and request.args.get("json") == "True":
        cbc_analysis_list = []

        query_result = CBCAnalysis.query.filter_by(patient_id=patient.id) \
                            .order_by(desc("updated_at")).all()
        for cbc_analysis in query_result:
            cbc_analysis_list.append(cbc_analysis.serialize())

        return json.dumps(cbc_analysis_list)



""" Delete Patient """
@app.route('/patients/delete/<int:patient_id>', methods=['POST'])
@login_required
@officer_permission.require(http_exception=403)
def delete_patient(patient_id=None):
    patient = Patient.query.get(patient_id)
    messages_list = {}

    if db_delete_patient(patient) == False:
        messages_list["error"] = MSG["OPERATION_FAILED"]

    else:
        messages_list["success"] = MSG["USER_PROFILE_DELETE_DONE"]

    return json.dumps(messages_list)


def db_update_or_insert_patient(patient):
    patient.updated_at = datetime.now()

    try:
        db.session.add(patient)
        db.session.commit()

        return True

    except Exception as e:
        print e.message
        db.session.rollback()

        return False

def db_delete_patient(patient):
    try:
        db.session.delete(patient)
        db.session.commit()

        return True

    except Exception as e:
        print e.message
        db.session.rollback()

        return False
