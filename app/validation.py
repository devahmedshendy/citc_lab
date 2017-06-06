from wtforms import Form, StringField, validators


class LoginForm(Form):
    user_username = StringField('user_username', [validators.InputRequired()])
    user_password = StringField('user_password', [validators.InputRequired()])
