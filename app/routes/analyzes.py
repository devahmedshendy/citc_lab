from flask            import current_app, request, session, url_for, redirect, \
                             render_template, flash, Response, abort
from flask_principal  import Permission, RoleNeed, Identity, identity_changed, \
                             identity_loaded, UserNeed, AnonymousIdentity
from flask_login      import login_user, login_required, logout_user, current_user
from flask_weasyprint import HTML, render_pdf

from app import app, db, login_manager
from app.models import *
from app.forms import *
from app.constants import *
from app.permissions import *
from app.services import *

from datetime import datetime
from sqlalchemy import desc, or_, and_
import json, jsonify


analyzes_joined_patient_columns = [
    Patient.id.label("patient_id"),
    Patient.personal_id.label("patient_personal_id"),
    Patient.name.label("patient_name"),
    Patient.age.label("patient_age"),
    Patient.gender.label("patient_gender"),
    CBCAnalysis.id.label("cbc_id"),
    CBCAnalysis.comment.label("cbc_comment"),
    CBCAnalysis.comment_doctor.label("cbc_comment_doctor"),
    CBCAnalysis.WCB.label("cbc_wcb"),
    CBCAnalysis.HGB.label("cbc_hgb"),
    CBCAnalysis.MCV.label("cbc_mcv"),
    CBCAnalysis.MCH.label("cbc_mch"),
    CBCAnalysis.approved.label("cbc_approved"),
    CBCAnalysis.approved_at.label("cbc_approved_at")
]

analysis_joined_patient_columns = [
    Patient.id.label("patient_id"),
    Patient.personal_id.label("patient_personal_id"),
    Patient.name.label("patient_name"),
    Patient.age.label("patient_age"),
    Patient.gender.label("patient_gender"),
    CBCAnalysis.id.label("cbc_id"),
    CBCAnalysis.comment.label("cbc_comment"),
    CBCAnalysis.comment_doctor.label("cbc_comment_doctor"),
    CBCAnalysis.WCB.label("cbc_wcb"),
    CBCAnalysis.HGB.label("cbc_hgb"),
    CBCAnalysis.MCV.label("cbc_mcv"),
    CBCAnalysis.MCH.label("cbc_mch"),
    CBCAnalysis.approved.label("cbc_approved"),
    CBCAnalysis.approved_at.label("cbc_approved_at"),
    CBCAnalysis.created_at.label("cbc_created_at")
]


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

            analyzes = paginated_analyzes_joined_patient_like_filter(
                'cbc',
                'cbc_id',
                Patient.personal_id,
                analyzes_joined_patient_columns,
                [page, PER_PAGE["ANALYZES"], False],
                search_string + "%"
            )

        except ValueError:
            analyzes = paginated_analyzes_joined_patient_like_filter(
                'cbc',
                'cbc_id',
                Patient.name,
                analyzes_joined_patient_columns,
                [page, PER_PAGE["ANALYZES"], False],
                search_string + "%"
            )

    else:
        print 'ererere'
        analyzes = paginated_analyzes_joined_patient(
            'cbc',
            'cbc_id',
            analyzes_joined_patient_columns,
            [page, PER_PAGE["ANALYZES"], False]
        )

    tempate = 'analyzes.html'
    return render_template(tempate, analyzes=analyzes, page=page)



""" Add Analysis """
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/new', methods=['POST'])
@login_required
@officer_permission.require(http_exception=403)
def add_analysis(analysis_type=None, patient_id=None):
    messages_list = {}

    print patient_id
    cbc_submitted_data = request.get_json()

    cbc_analysis = CBCAnalysis(
                    cbc_submitted_data["WCB"],
                    cbc_submitted_data["HGB"],
                    cbc_submitted_data["MCV"],
                    cbc_submitted_data["MCH"],
                    ANALYSIS_TO_ID[analysis_type],
                    patient_id)

    cbc_analysis_form = CBCAnalysisForm(obj=cbc_analysis)

    if cbc_analysis_form.validate_on_submit() == False:
        messages_list["error"] = []

        for field, errors in cbc_analysis_form.errors.items():
            for error in errors:
                messages_list["error"].append(error)

    else:
        try:
            db.session.add(cbc_analysis)
            db.session.commit()

            messages_list["success"] = MSG["CBC_ANALYSIS_ADD_DONE"]

        except sqlalchemy.exc.DatabaseError as e:
            print e.message
            db.session.rollback()

            messages_list["error"] = []
            messages_list["error"].append(MSG["OPERATION_FAILED"])


    return json.dumps(messages_list)



""" Edit Analysis """
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/edit/<int:analysis_id>', methods=["POST"])
@login_required
@officer_permission.require(http_exception=403)
def edit_analysis(analysis_type=None, analysis_id=None, patient_id=None):
    messages_list = {}

    print patient_id
    cbc_analysis = analysis_of_id(analysis_type, analysis_id)

    if not cbc_analysis:
        messages_list["error"] = [ MSG["NO_SUCH_ANALYSIS"] ]

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

    else:
        cbc_analysis_form.populate_obj(cbc_analysis)

        try:
            db.session.add(cbc_analysis)
            db.session.commit()

            messages_list["success"] = MSG["CBC_ANALYSIS_EDIT_DONE"]

        except sqlalchemy.exc.DatabaseError as e:
            print e.message
            db.session.rollback()

            messages_list["error"] = [ MSG["OPERATION_FAILED"] ]


    return json.dumps(messages_list)



""" Delete Analysis """
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/<int:analysis_id>/delete', methods=["GET"])
@app.route('/analyzes/<string:analysis_type>/<int:analysis_id>/delete', methods=["POST"])
@login_required
@officer_permission.require(http_exception=403)
def delete_analysis(analysis_type=None, analysis_id=None, patient_id=None):
    messages_list = {}

    cbc_analysis = analysis_of_id(analysis_type, analysis_id)

    if not cbc_analysis:
        messages_list["error"] = [ MSG["NO_SUCH_ANALYSIS"] ]

        return json.dumps(messages_list)

    try:
        db.session.delete(cbc_analysis)
        db.session.commit()

        messages_list["success"] = MSG["CBC_ANALYSIS_DELETE_DONE"]

    except sqlalchemy.exc.DatabaseError as e:
        print e.message
        db.session.rollback()

        messages_list["error"] = [ MSG["OPERATION_FAILED"] ]

    return json.dumps(messages_list)



""" Approve Analysis """
@app.route('/analyzes/<string:analysis_type>/<int:analysis_id>/approve', methods=["POST"])
@login_required
@doctor_permission.require(http_exception=403)
def approve_analysis(analysis_type=None, analysis_id=None):
    messages_list = {}

    submitted_data = request.get_json()

    cbc_analysis = analysis_of_id(analysis_type, analysis_id)

    if not cbc_analysis:
        messages_list["error"] = []
        messages_list["error"].append(MSG["NO_SUCH_ANALYSIS"] )

        return json.dumps(messages_list)

    cbc_analysis.approve()
    cbc_analysis.comment  = submitted_data["comment"]
    cbc_analysis.comment_doctor = current_user.firstname.title() + " " + current_user.lastname.title()
    cbc_analysis.updated_at = datetime.now()

    try:
        db.session.add(cbc_analysis)
        db.session.commit()

        messages_list["success"] = MSG["CBC_ANALYSIS_APPROVED"]

    except sqlalchemy.exc.DatabaseError as e:
        print e.message
        db.session.rollback()

        messages_list["error"] = MSG["OPERATION_FAILED"]

    return json.dumps(messages_list)


""" Get Analysis As PDF """
# This needs https://www.cairographics.org/download/ to be installed \
# in the server hosting this website.
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/<int:analysis_id>/pdf', methods=["GET"])
@login_required
def get_analysis_as_pdf(analysis_type=None, analysis_id=None, patient_id=None):
    if analysis_type == 'cbc':
        cbc_analysis = analysis_joined_patient_eq_filter(
            'cbc',
            analysis_id,
            analysis_joined_patient_columns
        )

        # cbc_analysis = CBCAnalysis.query \
        #                     .join(Patient, Patient.id==CBCAnalysis.patient_id) \
        #                     .filter(CBCAnalysis.id == analysis_id) \
        #                     .add_columns(Patient.personal_id,
        #                                 Patient.name,
        #                                 Patient.age,
        #                                 Patient.gender,
        #                                 CBCAnalysis.id,
        #                                 CBCAnalysis.comment,
        #                                 CBCAnalysis.comment_doctor,
        #                                 CBCAnalysis.WCB,
        #                                 CBCAnalysis.HGB,
        #                                 CBCAnalysis.MCV,
        #                                 CBCAnalysis.MCH,
        #                                 CBCAnalysis.created_at,
        #                                 CBCAnalysis.approved,
        #                                 CBCAnalysis.approved_at,
        #                                 CBCAnalysis.updated_at).first()




        if (not cbc_analysis):
            abort(404)
            # messages_list["error"] = []
            # messages_list["error"].append(MSG["NO_SUCH_ANALYSIS"] )
            #
            # return json.dumps(messages_list)


        template = 'analysis_as_pdf.html'
        html = render_template(template, analysis=cbc_analysis)
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
