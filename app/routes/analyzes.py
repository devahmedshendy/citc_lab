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
from sqlalchemy import desc, or_, and_, text
import json, jsonify


required_columns_for_analyzes = [
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
    CBCAnalysis.approved_at.label("cbc_created_at")
]

required_columns_for_analysis = [
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
    order_field           = 'cbc_id'
    pagination_properties = [page, PER_PAGE["ANALYZES"], False]
    search_string         = request.args.get('str')


    if request.args.get('not_approved_yet') == "on":
        not_approved_yet = True
    else:
        not_approved_yet = False


    if search_string and not_approved_yet:
        search_string = search_string.strip()
        filters       = [ text("cbc_approved=0") ]

        try:
            int(search_string)

            analyzes = search_for_personal_id(
                search_string=search_string + "%",
                order_field=order_field,
                required_columns=required_columns_for_analyzes,
                pagination_properties=pagination_properties,
                filters=filters
            )

        except ValueError:
            analyzes = search_for_patient_name(
                search_string=search_string + "%",
                order_field=order_field,
                required_columns=required_columns_for_analyzes,
                pagination_properties=pagination_properties,
                filters=filters
            )


    elif search_string and not not_approved_yet:
        search_string = search_string.strip()

        try:
            int(search_string)

            analyzes = search_for_personal_id(
                search_string=search_string + "%",
                order_field=order_field,
                required_columns=required_columns_for_analyzes,
                pagination_properties=pagination_properties,
            )

        except ValueError:
            analyzes = search_for_patient_name(
                search_string=search_string + "%",
                order_field=order_field,
                required_columns=required_columns_for_analyzes,
                pagination_properties=pagination_properties
            )


    elif not_approved_yet:
        filters       = [ text("cbc_analysis_approved=0") ]

        analyzes = get_all_analyzes_joined_patient(
            order_field=order_field,
            required_columns=required_columns_for_analyzes,
            pagination_properties=pagination_properties,
            filters=filters
        )


    else:
        analyzes = get_all_analyzes_joined_patient(
            order_field=order_field,
            required_columns=required_columns_for_analyzes,
            pagination_properties=pagination_properties
        )


    tempate = 'analyzes.html'
    return render_template(tempate, not_approved_yet=not_approved_yet, analyzes=analyzes, page=page)



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

    cbc_analysis_form = EditCBCAnalysisForm(obj=cbc_analysis)

    if cbc_analysis_form.validate_on_submit() == False:
        messages_list["error"] = []

        for field, errors in cbc_analysis_form.errors.items():
            for error in errors:
                messages_list["error"].append(error)

    else:
        try:
            db.session.add(cbc_analysis)
            db.session.commit()

            messages_list["success"] = MSG["ANALYSIS_ADD_DONE"]

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

    cbc_analysis = get_analysis_of_id(analysis_type, analysis_id)

    if not cbc_analysis:
        messages_list["error"] = [ MSG["NO_SUCH_ANALYSIS"] ]

        return json.dumps(messages_list)

    if cbc_analysis.approved:
        messages_list["error"] = [ MSG["APPROVED_ANALYSIS_EDIT_DENIED"] ]

        return json.dumps(messages_list)

    cbc_submitted_data = request.get_json()

    cbc_analysis_form = EditCBCAnalysisForm()

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

            messages_list["success"] = MSG["ANALYSIS_EDIT_DONE"]

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

    cbc_analysis = get_analysis_of_id(analysis_type, analysis_id)

    if not cbc_analysis:
        messages_list["error"] = [ MSG["NO_SUCH_ANALYSIS"] ]

        return json.dumps(messages_list)

    try:
        db.session.delete(cbc_analysis)
        db.session.commit()

        messages_list["success"] = MSG["ANALYSIS_DELETE_DONE"]

    except sqlalchemy.exc.DatabaseError as e:
        print e.message
        db.session.rollback()

        messages_list["error"] = [ MSG["OPERATION_FAILED"] ]

    return json.dumps(messages_list)



""" Approve Analysis """
@app.route('/analyzes/<string:analysis_type>/<int:analysis_id>/approve', methods=["GET", "POST"])
@login_required
@doctor_permission.require(http_exception=403)
def approve_analysis(analysis_type=None, analysis_id=None):
    cbc_analysis = get_analysis_of_id(analysis_type, analysis_id)

    if not cbc_analysis:
        abort(404)

    if request.method == "GET":
        if cbc_analysis.approved:
            flash_message = (MSG["ANALYSIS_ALREADY_APPROVED"], "error")
            flash(*flash_message)

            url = url_for('get_analyzes')
            response = redirect(url)

        else:
            patient = get_patient(patient_id=cbc_analysis.patient_id)

            template = "approve_cbc_analysis.html"
            response = render_template(template, analysis=cbc_analysis, patient=patient)


    elif request.method == "POST":
        cbc_analysis.approve()
        cbc_analysis.comment = request.form.get("comment")
        cbc_analysis.comment_doctor = current_user.firstname.title() + " " + current_user.lastname.title()
        cbc_analysis.updated_at = datetime.now()

        try:
            db.session.add(cbc_analysis)
            db.session.commit()

            flash_message = (MSG["ANALYSIS_APPROVE_DONE"], "success")
            flash(*flash_message)

        except sqlalchemy.exc.DatabaseError as e:
            print e.message
            db.session.rollback()

            flash_message = (MSG["OPERATION_FAILED"], "error")
            flash(*flash_message)

        url = url_for("get_analyzes", page=request.args.get('page'), not_approved_yet=request.args.get("not_approved_yet"))
        response = redirect(url)

    return response


""" Get Analysis As PDF """
# This needs https://www.cairographics.org/download/ to be installed \
# in the server hosting this website.
@app.route('/patients/<int:patient_id>/analyzes/<string:analysis_type>/<int:analysis_id>/print_as_pdf', methods=["GET"])
@login_required
def print_analysis(analysis_type=None, analysis_id=None, patient_id=None):
    if analysis_type == 'cbc':
        cbc_analysis = get_analysis_for_print(
            analysis_id=analysis_id,
            required_columns=required_columns_for_analysis
        )

        if (not cbc_analysis):
            abort(404)

        if not cbc_analysis.cbc_approved:
            flash_message = (MSG["ANALYSIS_NEED_APPROVE"], "error")
            flash(*flash_message)

            url = url_for("get_analyzes")
            response = redirect(url)

        else:
            template = 'analysis_as_pdf.html'
            html = render_template(template, analysis=cbc_analysis)
            response = render_pdf(HTML(string=html))

    return response
