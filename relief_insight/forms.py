from wtforms.form import Form
from wtforms.fields import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo

class ApplyOrganizationForm(Form):
    name = StringField(u'Organization name', validators = [
        InputRequired()
    ])
    email = StringField(u'Email', validators = [
        InputRequired(),
        Email()
    ])
    password = PasswordField(u'Password', validators = [
        InputRequired(),
        EqualTo(u'confirm_password', message = u'Passwords must match')
    ])
    confirm_password = PasswordField(u'Confirm password', validators = [
        InputRequired()
    ])

class LoginOrganizationForm(Form):
    email = StringField(u'Email', validators = [
        InputRequired(),
        Email()
    ])
    password = PasswordField(u'Password', validators = [
        InputRequired()
    ])

class SignUpRecipientForm(Form):
    phone_number = IntegerField(u'Phone number', validators = [
        InputRequired(),
    ])

    location = SelectField(u'Location', coerce=int, validators = [
        InputRequired()
    ])

class SendTextForm(Form):
    location = SelectField(u'Location', coerce=int, validators = [
        InputRequired()
    ])

    water = StringField(u'Water')
    medicine = StringField(u'Medicine')
    food = StringField(u'Food')
    clothing = StringField(u'Clothing')

    eta = StringField(u'Estimated time of arrival', validators = [
        InputRequired()
    ])
