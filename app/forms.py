from wtforms import validators, StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, optional, length
from flask_wtf import FlaskForm

from app import db
from app.models import User
from app.constants import *



class LoginForm(FlaskForm):
    username = StringField('username',
                        [InputRequired("Please enter your username.")])

    password = PasswordField('password',
                        [InputRequired("Please enter your password.")])



class AddUserFormForRoot(FlaskForm):
    firstname = StringField(u'Firstname',
                        [InputRequired("Please enter user's firstname.")],
                        render_kw={"placeholder": "Firstname",
                                    "class": "form-control"})

    lastname  = StringField(u'Lastname',
                        [InputRequired("Please enter user's lastname.")],
                        render_kw={"placeholder": "Lastname",
                                    "class": "form-control"})

    username  = StringField(u'Username',
                        [InputRequired("Please enter user's username.")],
                        render_kw={"placeholder": "Username",
                                    "class": "form-control"})

    password         = PasswordField(u'Password',
                         [InputRequired("Please enter user's password.")],
                         render_kw={"placeholder": "Password",
                                     "class": "form-control"})

    password_confirm  = PasswordField(u'Password Confirmation',
                            [
                                InputRequired("Please enter password confirmation."),
                                EqualTo('password_confirm', message="Passwords must match.")
                            ],
                            render_kw={"placeholder": "Password Confirmation",
                                        "class": "form-control"})

    role_id      = SelectField(u'Role',
                            [InputRequired("Please select a role.")],
                            choices=[
                                ("", "Select Role"),
                                ROLES["admin"],
                                ROLES["doctor"],
                                ROLES["officer"] ],
                            render_kw={"class": "form-control"})



class AddUserFormForAdmin(FlaskForm):
    firstname = StringField(u'Firstname',
                        [InputRequired("Please enter user's firstname.")],
                        render_kw={"placeholder": "Firstname",
                                    "class": "form-control"})

    lastname  = StringField(u'Lastname',
                        [InputRequired("Please enter user's lastname.")],
                        render_kw={"placeholder": "Lastname",
                                    "class": "form-control"})

    username  = StringField(u'Username',
                        [InputRequired("Please enter user's username.")],
                        render_kw={"placeholder": "Username",
                                    "class": "form-control"})

    password         = PasswordField(u'Password',
                         [InputRequired("Please enter user's password.")],
                         render_kw={"placeholder": "Password",
                                     "class": "form-control"})

    password_confirm  = PasswordField(u'Password Confirmation',
                            [
                                InputRequired("Please enter password confirmation."),
                                EqualTo('password_confirm', message="Passwords must match.")
                            ],
                            render_kw={"placeholder": "Password Confirmation",
                                        "class": "form-control"})

    role_id      = SelectField(u'Role',
                            [InputRequired("Please select a role.")],
                            choices=[
                                ("", "Select Role"),
                                ROLES["doctor"],
                                ROLES["officer"], ],
                            render_kw={"class": "form-control"})



class EditUserFormForAdmin(FlaskForm):
    firstname = StringField(u'Firstname',
                        [InputRequired("Please enter user's firstname.")],
                        render_kw={"placeholder": "Firstname",
                                    "class": "form-control"})

    lastname  = StringField(u'Lastname',
                        [InputRequired("Please enter user's lastname.")],
                        render_kw={"placeholder": "Lastname",
                                    "class": "form-control"})

    username  = StringField(u'Username',
                        [InputRequired("Please enter user's username.")],
                        render_kw={"placeholder": "Username",
                                    "class": "form-control"})

    role_id      = SelectField(u'Role',
                            choices=[
                                ("", "Select Role"),
                                ROLES["doctor"],
                                ROLES["officer"] ],
                            render_kw={"class": "form-control"})



class EditUserFormForRoot(FlaskForm):
    firstname = StringField(u'Firstname',
                        [InputRequired("Please enter user's firstname.")],
                        render_kw={"placeholder": "Firstname",
                                    "class": "form-control"})

    lastname  = StringField(u'Lastname',
                        [InputRequired("Please enter user's lastname.")],
                        render_kw={"placeholder": "Lastname",
                                    "class": "form-control"})

    username  = StringField(u'Username',
                        [InputRequired("Please enter user's username.")],
                        render_kw={"placeholder": "Username",
                                    "class": "form-control"})

    role_id      = SelectField(u'Role',
                            choices=[
                                ("", "Select Role"),
                                ROLES["admin"],
                                ROLES["doctor"],
                                ROLES["officer"] ],
                            render_kw={"class": "form-control"})



class EditAccountForm(FlaskForm):
    firstname = StringField(u'Firstname',
                        [InputRequired("Please enter your firstname.")],
                        render_kw={"placeholder": "Firstname",
                                    "class": "form-control"})

    lastname  = StringField(u'Lastname',
                        [InputRequired("Please enter your lastname.")],
                        render_kw={"placeholder": "Lastname",
                                    "class": "form-control"})

    username  = StringField(u'Username',
                        [InputRequired("Please enter your username.")],
                        render_kw={"placeholder": "Username",
                                    "class": "form-control"})



class ChangeUserPasswordForm(FlaskForm):
    new_password         = PasswordField(u'New Password',
                         [InputRequired("Please enter user's new password.")],
                         render_kw={"placeholder": "New Password",
                                     "class": "form-control"})

    new_password_confirm  = PasswordField(u'New Password Confirmation',
                            [
                                InputRequired("Please enter new password confirmation."),
                                EqualTo('new_password', message="Passwords must match.")
                            ],
                            render_kw={"placeholder": "New Password Confirmation",
                                        "class": "form-control"})



class ChangeAccountPasswordForm(FlaskForm):
    old_password         = PasswordField(u'Old Password',
                         [InputRequired("Please enter your old password.")],
                         render_kw={"placeholder": "Old Password",
                                     "class": "form-control"})

    new_password         = PasswordField(u'New Password',
                         [InputRequired("Please enter your new password.")],
                         render_kw={"placeholder": "New Password",
                                     "class": "form-control"})

    new_password_confirm  = PasswordField(u'New Password Confirmation',
                            [
                                InputRequired("Please enter new password confirmation."),
                                EqualTo('new_password', message="Passwords must match.")
                            ],
                            render_kw={"placeholder": "New Password Confirmation",
                                        "class": "form-control"})



class AddPatientForm(FlaskForm):
    personal_id = StringField(u'Persoanl ID',
                        [InputRequired("Please enter patient's ID.")],
                        render_kw={"placeholder": "Personal ID",
                                    "class": "form-control"})

    name        = StringField(u'Name',
                        [InputRequired("Please enter patient's name.")],
                        render_kw={"placeholder": "Name",
                                    "class": "form-control"})

    address     = StringField(u'Address',
                        [InputRequired("Please enter patient's address.")],
                        render_kw={"placeholder": "Address",
                                    "class": "form-control"})

    phone       = StringField(u'Phone',
                        [optional()],
                        render_kw={"placeholder": "Phone",
                                    "class": "form-control"})

    age         = IntegerField(u"Age",
                        [InputRequired("Please enter patient's age.")],
                        render_kw={"placeholder": "Age",
                                    "class": "form-control"})

    gender      = SelectField(u'Gender',
                        choices=[("Male", "Male"), ("Female", "Female")],
                                render_kw={"class": "form-control"})



class EditPatientForm(FlaskForm):
    personal_id = StringField(u'Personal ID',
                        [InputRequired("Please enter patient's ID.")],
                        render_kw={"placeholder": "Personal ID",
                                    "class": "form-control"})

    name        = StringField(u'Name',
                        [InputRequired("Please enter patient's name.")],
                        render_kw={"placeholder": "Name",
                                    "class": "form-control"})

    address     = StringField(u'Address',
                        [InputRequired("Please enter patient's address.")],
                        render_kw={"placeholder": "Address",
                                    "class": "form-control"})

    phone       = StringField(u'Phone',
                        [optional()],
                        render_kw={"placeholder": "Phone",
                                    "class": "form-control"})

    age         = IntegerField(u"Age",
                        [InputRequired("Please enter patient's age.")],
                        render_kw={"placeholder": "Age",
                                    "class": "form-control"})

    gender      = SelectField(u'Gender',
                        choices=[("Male", "Male"), ("Female", "Female")],
                                render_kw={"class": "form-control"})



class EditCBCAnalysisForm(FlaskForm):
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



class AddCBCForm(FlaskForm):
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
