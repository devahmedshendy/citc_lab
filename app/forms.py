from wtforms import validators, StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, optional, length
from flask_wtf import FlaskForm

from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('username',
                        [InputRequired("Please enter your username.")])

    password = PasswordField('password',
                        [InputRequired("Please enter your password.")])


class RegisterForm(FlaskForm):
    firstname = StringField('firstname',
                        [InputRequired("Please enter your firstname.")])

    lastname  = StringField('lastname',
                        [InputRequired("Please enter your lastname.")])

    username  = StringField('username',
                        [InputRequired("Please enter your username.")])

    password         = PasswordField('password',
                         [
                            InputRequired("Please enter your password."),
                            EqualTo('password_confirm', message="Passwords must match.")
                         ])

    password_confirm  = PasswordField('password_confirm',
                                [InputRequired("Please enter password confirmation.")])



class PatientForm(FlaskForm):
    personal_id = StringField(u'ID',
                        [InputRequired("Please enter patient's ID.")])

    name        = StringField(u'Name',
                        [InputRequired("Please enter patient's name.")])

    address     = StringField(u'Address',
                        [InputRequired("Please enter patient's address.")])

    phone       = StringField(u'Phone',
                        [optional()])

    age         = IntegerField(u"Age",
                        [InputRequired("Please enter patient's age.")])

    gender      = SelectField(u'Gender',
                        choices=[("Male", "Male"), ("Female", "Female")])


class CBCAnalysisForm(FlaskForm):
    comment  = TextAreaField('Comment',
                    [optional(), length(max=200)],
                    render_kw={"placeholder": "Doctor comments...", "rows": "3"})
                    
    WCB      = StringField('WBC',
                    [InputRequired("Please enter WBC value.")],
                    render_kw={"placeholder": "White Blod Cells"})
    HGB      = StringField('HGB',
                    [InputRequired("Please enter HGB value.")],
                    render_kw={"placeholder": "Hemoglibin"})

    MCV      = StringField('MCV',
                    [InputRequired("Please enter MCV value.")],
                    render_kw={"placeholder": "Mean Corpuscular Volume"})

    MCH      = StringField('MCH',
                    [InputRequired("Please enter MCH value.")],
                    render_kw={"placeholder": "Mean Cell Hemoglubine"})
