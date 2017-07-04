from app.models import *



# -----------------------------------------
#
#  Function to Fetch a Group of Analyzes
# -----------------------------------------
def search_for_personal_id(search_string, order_field,
                           required_columns, pagination_properties,
                           analysis_type='cbc', **kwargs):

    if analysis_type == 'cbc':
        analyzes = CBCAnalysis.query                                    \
                    .join(Patient)                                      \
                    .filter(Patient.personal_id.like(search_string))    \
                    .add_columns(*required_columns)                     \
                    .order_by(order_field)                              \

        if "filters" in kwargs:
            for filter in kwargs["filters"]:
                analyzes = analyzes.filter(filter)

    return analyzes.paginate(*pagination_properties)


def search_for_patient_name(search_string, order_field,
                            required_columns, pagination_properties,
                            analysis_type='cbc', **kwargs):

    if analysis_type == 'cbc':
        analyzes = CBCAnalysis.query                            \
                    .join(Patient)                              \
                    .filter(Patient.name.like(search_string))   \
                    .add_columns(*required_columns)             \
                    .order_by(order_field)                      \

        if "filters" in kwargs:
            for filter in kwargs["filters"]:
                analyzes = analyzes.filter(filter)

    return analyzes.paginate(*pagination_properties)


def get_all_analyzes_joined_patient(order_field, required_columns,
                                    pagination_properties, analysis_type='cbc',
                                    **kwargs):

    if analysis_type == 'cbc':
        analyzes = CBCAnalysis.query                  \
                    .join(Patient)                    \
                    .add_columns(*required_columns)   \
                    .order_by(order_field)            \

        if "filters" in kwargs:
            for filter in kwargs["filters"]:
                analyzes = analyzes.filter(filter)

    return analyzes.paginate(*pagination_properties)


def get_all_analyzes_of_patient(patient_id, analysis_type='cbc'):
    if analysis_type == 'cbc':
        analyzes =  CBCAnalysis.query                                   \
                        .filter(CBCAnalysis.patient_id == patient_id)   \
                        .all()

    return analyzes

# -----------------------------------------
#
#  Funcitons to Fetch Only One Analysis
# -----------------------------------------
def get_analysis_for_print(analysis_id, required_columns, analysis_type='cbc'):
    if analysis_type == 'cbc':
        analysis = CBCAnalysis.query                        \
                    .join(Patient)                          \
                    .filter(CBCAnalysis.id == analysis_id)  \
                    .add_columns(*required_columns)         \
                    .first()

    return analysis


def get_analysis_of_id(analysis_type, analysis_id):
    if analysis_type == 'cbc':
        analysis = CBCAnalysis.query.get(analysis_id)

    return analysis


def analysis_of_patient(analysis_type, analysis_id, patient_id):
    if analysis_type == 'cbc':
        return CBCAnalysis.query \
                    .filter(CBCAnalysis.patient_id == patient_id) \
                    .first()
