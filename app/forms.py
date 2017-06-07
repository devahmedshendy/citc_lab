from wtforms import Form, StringField, validators, PasswordField


class LoginForm(Form):
    user_username = StringField('user_username',
                        [validators.InputRequired("Please enter your username")])
    user_password = PasswordField('user_password',
                        [validators.InputRequired("Please enter your password")])


class RegisterForm(Form):
    user_firstname = StringField('user_firstname',
                        [validators.InputRequired("Please enter your firstname")])
    user_lastname  = StringField('user_lastname',
                        [validators.InputRequired("Please enter your lastname")])
    user_username  = StringField('user_username',
                        [validators.InputRequired("Please enter your username")])
    user_password  = PasswordField('user_password', [
        validators.InputRequired("Please enter your password"),
        validators.EqualTo('user_password_confirm', message="Passwords must match")
    ])
    user_password_confirm = PasswordField('user_password_confirm',
                                [validators.InputRequired("Please enter password confirmation")])
