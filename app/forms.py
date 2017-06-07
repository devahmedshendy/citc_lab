from wtforms import Form, validators, StringField, PasswordField, IntegerField, SelectField


class LoginForm(Form):
    user_username = StringField('user_username',
                        [validators.InputRequired("Please enter your username.")])

    user_password = PasswordField('user_password',
                        [validators.InputRequired("Please enter your password.")])


class RegisterForm(Form):
    user_firstname = StringField('user_firstname',
                        [validators.InputRequired("Please enter your firstname.")])

    user_lastname  = StringField('user_lastname',
                        [validators.InputRequired("Please enter your lastname.")])

    user_username  = StringField('user_username',
                        [validators.InputRequired("Please enter your username.")])

    user_password  = PasswordField('user_password',
                     [
                        validators.InputRequired("Please enter your password."),
                        validators.EqualTo('user_password_confirm', message="Passwords must match.")
                     ])

    user_password_confirm = PasswordField('user_password_confirm',
                                [validators.InputRequired("Please enter password confirmation.")])



class PatientForm(Form):
    patient_personal_id = StringField(u'Patient Personal ID',
                            [validators.InputRequired("Please enter patient's ID.")])

    patient_name        = StringField('patient_name',
                            [validators.InputRequired("Please enter patient's name.")])

    patient_address     = StringField('patient_address',
                            [validators.InputRequired("Please enter patient's address.")])

    patient_phone       = IntegerField('patient_phone',
                            [validators.optional()])

    patient_age         = IntegerField("patient_age",
                            [validators.InputRequired("Please enter patient's age.")])

    patient_gender      = SelectField(u'Patient Gender',
                            choices=[("male", "Male"), ("female", "Female")])
