from flask            import current_app, request, session, url_for, redirect, \
                             render_template, flash, Response
from flask_principal  import Permission, RoleNeed, Identity, identity_changed, \
                             identity_loaded, UserNeed, AnonymousIdentity
from flask_login      import login_user, login_required, logout_user, current_user
from flask_weasyprint import HTML, render_pdf

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
doctor_permission = Permission(be_investigation_doctor)
officer_permission = Permission(be_registration_officer)



""" Get Analyzes """
@app.route('/analyzes', methods=['GET'])
@app.route('/analyzes/page/<int:page>', methods=['GET'], endpoint='get_analyzes_by_page')
@login_required
def get_analyzes(page=1):
    search_string = request.args.get('str')

    if search_string:
        search_string = search_string.strip()

        try:

            int(search_string)
            analyzes = CBCAnalysis.query \
                        .join(Patient) \
                        .order_by(CBCAnalysis.updated_at.desc()) \
                        .add_columns(Patient.id.label("patient_id"),
                                    Patient.personal_id,
                                    Patient.name,
                                    Patient.age,
                                    Patient.gender,
                                    CBCAnalysis.id,
                                    CBCAnalysis.comment,
                                    CBCAnalysis.comment_doctor,
                                    CBCAnalysis.WCB,
                                    CBCAnalysis.HGB,
                                    CBCAnalysis.MCV,
                                    CBCAnalysis.MCH,
                                    CBCAnalysis.approved,
                                    CBCAnalysis.approved_at) \
                        .filter(Patient.personal_id.op('regexp')("^" + search_string + "")) \
                        .paginate(page, PER_PAGE["ANALYZES"], False)

        except ValueError:
            analyzes = CBCAnalysis.query \
                        .join(Patient) \
                        .order_by(CBCAnalysis.updated_at.desc()) \
                        .add_columns(Patient.id.label("patient_id"),
                                    Patient.personal_id,
                                    Patient.name,
                                    Patient.age,
                                    Patient.gender,
                                    CBCAnalysis.id,
                                    CBCAnalysis.comment,
                                    CBCAnalysis.comment_doctor,
                                    CBCAnalysis.WCB,
                                    CBCAnalysis.HGB,
                                    CBCAnalysis.MCV,
                                    CBCAnalysis.MCH,
                                    CBCAnalysis.approved,
                                    CBCAnalysis.approved_at) \
                        .filter(Patient.name.op('regexp')("^" + search_string + "")) \
                        .paginate(page, PER_PAGE["ANALYZES"], False)

    else:
        analyzes = CBCAnalysis.query \
                                .join(Patient) \
                                .order_by(CBCAnalysis.updated_at.desc()) \
                                .add_columns(Patient.id.label("patient_id"),
                                            Patient.personal_id,
                                            Patient.name,
                                            Patient.age,
                                            Patient.gender,
                                            CBCAnalysis.id,
                                            CBCAnalysis.comment,
                                            CBCAnalysis.comment_doctor,
                                            CBCAnalysis.WCB,
                                            CBCAnalysis.HGB,
                                            CBCAnalysis.MCV,
                                            CBCAnalysis.MCH,
                                            CBCAnalysis.approved,
                                            CBCAnalysis.approved_at) \
                                .paginate(page, PER_PAGE["ANALYZES"], False)

    tempate = 'analyzes.html'
    return render_template(tempate, analyzes=analyzes, page=page)



""" Add Analysis """
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/new', methods=['POST'])
@login_required
@officer_permission.require(http_exception=403)
def add_analysis(patient_id=None, analysis_type=None):
    messages_list = {}

    cbc_submitted_data = request.get_json()

    cbc_analysis = CBCAnalysis(
                    cbc_submitted_data["WCB"],
                    cbc_submitted_data["HGB"],
                    cbc_submitted_data["MCV"],
                    cbc_submitted_data["MCH"],
                    ANALYSIS_TO_ID[analysis_type],
                    patient_id)

    print cbc_analysis.approved

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
@officer_permission.require(http_exception=403)
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
@officer_permission.require(http_exception=403)
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


""" Approve Analysis """
@app.route('/analyzes/<string:analysis_type>/<int:analysis_id>/approve', methods=["POST"])
@login_required
@doctor_permission.require(http_exception=403)
def approve_analysis(analysis_type=None, analysis_id=None):
    messages_list = {}

    submitted_data = request.get_json()

    print submitted_data
    cbc_analysis = CBCAnalysis.query.get(analysis_id)

    if not cbc_analysis:
        messages_list["error"] = []
        messages_list["error"].append(MSG["NO_SUCH_CBC_ANALYSIS"] )

        return json.dumps(messages_list)

    cbc_analysis.approve()
    cbc_analysis.comment  = submitted_data["comment"]
    cbc_analysis.comment_doctor = current_user.firstname.title() + " " + current_user.lastname.title()

    if db_update_or_insert_analysis(cbc_analysis) == False:
        messages_list["error"] = MSG["OPERATION_FAILED"]

    else:
        messages_list["success"] = MSG["CBC_ANALYSIS_APPROVED"]

    return json.dumps(messages_list)


""" Get Analysis As PDF """
# This needs https://www.cairographics.org/download/ to be installed \
# in the server hosting this website.
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/<int:analysis_id>/pdf', methods=["GET"])
@login_required
def get_analysis_as_pdf(patient_id=None, analysis_type=None, analysis_id=None):
    messages_list = {}

    if analysis_type == 'cbc':
        cbc_analysis = CBCAnalysis.query \
                            .join(Patient, Patient.id==CBCAnalysis.patient_id) \
                            .filter(CBCAnalysis.id == analysis_id) \
                            .add_columns(Patient.personal_id,
                                        Patient.name,
                                        Patient.age,
                                        Patient.gender,
                                        CBCAnalysis.id,
                                        CBCAnalysis.comment,
                                        CBCAnalysis.comment_doctor,
                                        CBCAnalysis.WCB,
                                        CBCAnalysis.HGB,
                                        CBCAnalysis.MCV,
                                        CBCAnalysis.MCH,
                                        CBCAnalysis.created_at,
                                        CBCAnalysis.approved,
                                        CBCAnalysis.approved_at,
                                        CBCAnalysis.updated_at).first()




        if (not cbc_analysis):
            messages_list["error"] = []
            messages_list["error"].append(MSG["NO_SUCH_CBC_ANALYSIS"] )

            return json.dumps(messages_list)


        template = 'analysis_as_pdf.html'
        html = render_template(template, cbc=cbc_analysis)
        return render_pdf(HTML(string=html))



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
