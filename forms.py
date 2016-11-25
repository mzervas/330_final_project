from flask_wtf import Form
from wtforms.fields import TextField, BooleanField, SubmitField, HiddenField
# from wtforms.validators import Required

class Login(Form):
    email = TextField("Email")
    password = TextField("Password")
    token = HiddenField("Token", id='token')

    submit = SubmitField("View my artists")
