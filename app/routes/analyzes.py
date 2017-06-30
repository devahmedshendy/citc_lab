from flask            import current_app, request, session, url_for, redirect, \
                             render_template, flash
from flask_principal  import Permission, RoleNeed, Identity, identity_changed, \
                             identity_loaded, UserNeed, AnonymousIdentity
from flask_login      import login_user, login_required, logout_user, current_user

from app import app, db, login_manager
from app.models import *
from app.forms import *
from app.constants import *

from datetime import datetime
from sqlalchemy import desc, or_, and_
import json, jsonify

# Needs - Roles
be_investigation_doctor = RoleNeed('investigation_doctor')
be_registration_officer = RoleNeed('registration_officer')

# Permissions
investigation_doctor_permission = Permission(be_investigation_doctor)
registration_officer_permission = Permission(be_registration_officer)


""" Add Analysis """
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/new', methods=['POST'])
@login_required
@registration_officer_permission.require(http_exception=403)
def add_analysis(patient_id=None, analysis_type=None):
    messages_list = {}

    cbc_submitted_data = request.get_json()

    cbc_analysis = CBCAnalysis(
                    cbc_submitted_data["WCB"],
                    cbc_submitted_data["HGB"],
                    cbc_submitted_data["MCV"],
                    cbc_submitted_data["MCH"],
                    ANALYSIS_TO_ID[analysis_type],
                    patient_id,
                    cbc_submitted_data["comment"])

    cbc_analysis_form = CBCAnalysisForm(obj=cbc_analysis)

    if cbc_analysis_form.validate_on_submit() == False:
        print "validation error"
        messages_list["error"] = []

        for field, errors in cbc_analysis_form.errors.items():
            for error in errors:
                messages_list["error"].append(error)

        return json.dumps(messages_list)


    if cbc_analysis_form.validate_on_submit() == True:
        if db_update_or_insert_analysis(cbc_analysis) == False:
            messages_list["error"] = []
            messages_list["error"].append(MSG["OPERATION_FAILED"])
            return json.dumps(messages_list)

        else:
            messages_list["success"] = MSG["CBC_ANALYSIS_ADD_DONE"]
            return json.dumps(messages_list)




""" Edit Analysis """
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/edit/<int:analysis_id>', methods=["POST"])
@login_required
@registration_officer_permission.require(http_exception=403)
def edit_analysis(patient_id=None, analysis_type=None, analysis_id=None):
    messages_list = {}

    cbc_analysis = CBCAnalysis.query \
                        .join(Patient, Patient.id==CBCAnalysis.patient_id) \
                        .filter(CBCAnalysis.id == analysis_id) \
                        .first()


    if (not cbc_analysis):
        messages_list["error"] = []
        messages_list["error"].append(MSG["NO_SUCH_CBC_ANALYSIS"] )

        return json.dumps(messages_list)


    cbc_submitted_data = request.get_json()

    cbc_analysis_form = CBCAnalysisForm()

    print cbc_submitted_data["comment"]
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

        if db_update_or_insert_analysis(cbc_analysis) == False:
            messages_list["error"] = []
            messages_list["error"].append(MSG["OPERATION_FAILED"])
            return json.dumps(messages_list)

        else:
            messages_list["success"] = MSG["CBC_ANALYSIS_EDIT_DONE"]
            return json.dumps(messages_list)


""" Delete Analysis """
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/<int:analysis_id>/delete', methods=["GET"])
@app.route('/analyzes/<string:analysis_type>/<int:analysis_id>/delete', methods=["POST"])
@login_required
@registration_officer_permission.require(http_exception=403)
def delete_analysis(patient_id=None, analysis_type=None, analysis_id=None):
    messages_list = {}

    print analysis_id
    cbc_analysis = CBCAnalysis.query.get(analysis_id)

    if not cbc_analysis:
        messages_list["error"] = []
        messages_list["error"].append(MSG["NO_SUCH_CBC_ANALYSIS"] )

        return json.dumps(messages_list)

    if db_delete_analysis(cbc_analysis) == False:
        messages_list["error"] = MSG["OPERATION_FAILED"]

    else:
        messages_list["success"] = MSG["CBC_ANALYSIS_DELETE_DONE"]

    return json.dumps(messages_list)


def db_update_or_insert_analysis(cbc):
    cbc.updated_at = datetime.now()

    try:
        db.session.add(cbc)
        db.session.commit()

        return True

    except Exception as e:
        print e.message
        db.session.rollback()

        return False

def db_delete_analysis(cbc):
    try:
        db.session.delete(cbc)
        db.session.commit()

        return True

    except Exception as e:
        print e.message
        db.session.rollback()

        return False
