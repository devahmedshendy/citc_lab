from sqlalchemy import desc, or_, and_

from app.models import *

def get_patient(patient_id=None, personal_id=None):
    patient = None
    if patient_id:
        return Patient.query.get(patient_id)

    elif personal_id:
        return Patient.query.filter_by(personal_id=personal_id).first()

    return patient

def patient_of_personal_id(personal_id=None):
    return Patient.query.filter_by(personal_id=personal_id).first()

def patient_of_id(patient_id=None):
    return Patient.query.get(patient_id)
