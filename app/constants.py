MSG = {
    # Authentication - Success Messages
    'LOGIN_DONE'                    : 'Login successful for ',
    'LOGOUT_DONE'                   : 'Logout done successfully.',
    'LOGIN_REQUIRED'                : 'You have to login first.',

    # Users - Success Messages
    'USER_PROFILE_CREATE_DONE'      : 'User profile has been created successfully!',
    'USER_PROFILE_EDIT_DONE'        : 'User profile has been edited successfully!',
    'USER_PASSWORD_CHANGE_DONE'     : 'Password has been changed successfully!',
    'USER_PROFILE_DELETE_DONE'      : 'User profile has been deleted successfully!',

    # Users - Error Messages
    'NO_SUCH_USER'                  : 'Sorry, but there is no such user in our system.',
    'WRONG_CREDENTIALS'             : 'You provided wrong credentials, please try again.',
    'WRONG_OLD_PASSWORD'            : 'Old password is not correct.',
    'USER_PROFILE_DELETE_DENIED'    : 'This can not be deleted.',
    'USERNAME_IS_NOT_AVAILABLE'     : 'This username is not available.',
    'DUPLICATE_USER'                : 'This username is already registered.',

    # Patients - Success Messages
    'PATIENT_PROFILE_CREATE_DONE'   : 'Patient has been added successfully!',
    'PATIENT_PROFILE_EDIT_DONE'     : 'Patient has been updated successfully!',
    'PATIENT_PROFILE_DELETE_DONE'   : 'Patient profile has been delete successfully!',

    # Patients - Error Messages
    'DUPLICATE_PERSONAL_ID'         : 'This personal id is already added for patient %s.',
    'INVALID_PERSONAL_ID'           : 'Please enter a valid personal id.',
    'NO_SUCH_PATIENT'               : 'There is no such patient in the system.',

    # CBC Analysis - Success Messages
    'CBC_ANALYSIS_ADD_DONE'         : 'The CBC Analysis has been added successfully!',
    'CBC_ANALYSIS_EDIT_DONE'        : 'The CBC Analysis has been edited successfully!',
    'CBC_ANALYSIS_DELETE_DONE'      : 'The CBC Analysis has been deleted successfully!',
    'CBC_ANALYSIS_APPROVED'         : 'The CBC Analysis has been approved!',

    # CBC Analysis - Error Messages
    'NO_SUCH_ANALYSIS'          : 'No such analysis for this patient.',

    # General Error Messages
    'UNEXPECTED_ERROR'              : 'Unexpected error.',
    'NO_DATA_SUBMITTED'             : 'No data has been submitted, please check with admin',
    'OPERATION_FAILED'              : 'Operation failed.',
    '403'                           : 'You are not authorized to access this page.',
}

PER_PAGE = {
    'USERS'     : 10,
    'PATIENTS'  : 10,
    'ANALYZES'  : 10,
}

ANALYSIS_TO_ID = {
    'cbc'       : 1,
}

ROLES = {
    'root'      :   ("10", 'root'),
    'admin'     :   ("20", 'admin'),
    'doctor'    :   ("30", 'doctor'),
    'officer'   :   ("40", 'officer')
}
