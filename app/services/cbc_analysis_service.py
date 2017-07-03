# from sqlalchemy import desc, or_, and_

from app.models import *



def analysis_of_id(analysis_type, analysis_id):
    if analysis_type == 'cbc':
        return CBCAnalysis.query.get(analysis_id)


def analysis_of_patient(analysis_type, analysis_id, patient_id):
    if analysis_type == 'cbc':
        return CBCAnalysis.query \
                    .filter(CBCAnalysis.patient_id == patient_id) \
                    .first()


def analyzes_of_patient_in_desc_order(analysis_type, patient_id, order_field):
    if analysis_type == 'cbc':
        return CBCAnalysis.query \
                .filter(CBCAnalysis.patient_id == patient_id) \
                .order_by(order_field).all()


def analyzes_of_patient_in_desc_order(analysis_type, patient_id, order_field):
    if analysis_type == 'cbc':
        return CBCAnalysis.query \
                .filter(CBCAnalysis.patient_id == patient_id) \
                .order_by(order_field.desc()).all()


def analysis_joined_patient_eq_filter(analysis_type, filter_field, columns):
    if analysis_type == 'cbc':
        return CBCAnalysis.query \
                .join(Patient, Patient.id == CBCAnalysis.patient_id) \
                .filter(CBCAnalysis.id == filter_field) \
                .add_columns(*columns) \
                .first()


def paginated_analyzes_joined_patient(analysis_type, order, columns, page_param):
    if analysis_type == 'cbc':
        return CBCAnalysis.query.join(Patient) \
                .order_by(order) \
                .add_columns(*columns) \
                .paginate(*page_param) \


def paginated_analyzes_joined_patient_like_filter(analysis_type, order, filter_field, columns, page_param, search_string):
    if analysis_type == 'cbc':
        return CBCAnalysis.query.join(Patient) \
                .order_by(order) \
                .filter(filter_field.like(search_string)) \
                .add_columns(*columns) \
                .paginate(*page_param) \



# def query_analysis(analysis_model):
#     return analysis_model.query
#
#
# def eq_(query, filter_field, value):
#     return query.filter(filter_field == value)
#
# def startswith_(query, filter_field, value):
#     return query.filter(filter_field.startswith_(value))
#
# def order_(query, order_field):
#     return query.order_by(order_field)
#
# def join_(query, joined_model):
#     return query.join(joined_model)
