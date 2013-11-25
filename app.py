import os

from helpers import is_prod
from flask import Flask, request, render_template, redirect, flash, url_for
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from forms import ApplyOrganizationForm, LoginOrganizationForm, SignUpRecipientForm, SendTextForm
from models import Organization, Location, Recipient
from twilio.rest import TwilioRestClient

# constants
TEXT_FORMAT = ','.join([
    'Loc:{location}',
    'Water:{water}',
    'Meds:{medicine}',
    'Food:{food}',
    'Clothes:{clothing}',
    'ETA:{eta}'
])

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = os.environ['TWILIO_PHONE_NUMBER']

# app
app = Flask(__name__)

# database
if is_prod():
    app.secret_key = os.environ['RELIEF_INSIGHT_SECRET_KEY']
else:
    app.secret_key = 'ruf4biun4fib4iu2i3u42398rhuibe'

# login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Organization.get(Organization.id == id)

def login_organization(form):
    try:
        organization = Organization.authenticate(
            form.email.data,
            form.password.data
        )

        login_user(organization, remember=True)
    except:
        pass

# forms
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginOrganizationForm()

    if request.method == 'POST':
        form.process(request.form)
        if form.validate():
            login_organization(form)

    if current_user.is_authenticated():
        return redirect(url_for('organizations_dashboard'))

    return render_template('index.html', form = form)

@app.route('/recipients/sign-up/', methods=['GET', 'POST'])
def recipients_sign_up():
    form = SignUpRecipientForm()
    form.location.choices = Location.get_choices()

    if request.method == 'POST':
        form.process(request.form)
        if form.validate():
            recipient = Recipient.new(
                form.phone_number.data,
                form.location.data
            )
            recipient.save()

    return render_template('recipients/sign-up.html',
                           form = form)

@app.route('/organizations/apply/', methods=['GET', 'POST'])
def organizations_apply():
    form = ApplyOrganizationForm()

    if request.method == 'POST':
        form.process(request.form)
        if form.validate():
            organization = Organization.new(
                form.name.data,
                form.email.data,
                form.password.data
            )

            organization.save()

    return render_template('organizations/apply.html',
                           form = form)

@app.route('/organizations/dashboard/', methods=['GET', 'POST'])
@login_required
def organizations_dashboard():
    form = SendTextForm()
    form.location.choices = Location.get_choices()

    if request.method == 'POST':
        form.process(request.form)

        if form.validate():
            send_text_messages(form)
            flash('Your message was successfully sent!')

    return render_template('organizations/dashboard.html',
                           form = form)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def send_text_messages(form):
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    if form.validate():
        location = Location.get(
            Location.id == form.location.data
        )

        message_body = TEXT_FORMAT.format(
            location = location.get_short_name(),
            water = form.water.data,
            medicine = form.medicine.data,
            food = form.food.data,
            clothing = form.clothing.data,
            eta = form.eta.data
        )

        for recipient in location.recipient_set:
            message = client.messages.create(
                to = recipient.phone_number,
                from_ = TWILIO_NUMBER,
                body = message_body
            )

if __name__ == '__main__':
    app.run(debug=True)
