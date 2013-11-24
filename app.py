from helpers import is_prod
from flask import Flask, request, render_template, redirect, flash, url_for
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from forms import ApplyOrganizationForm, LoginOrganizationForm, SignUpRecipientForm
from models import Organization, Location, Recipient
from twilio.rest import TwilioRestClient

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
            request.form['email'],
            request.form['password']
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
                request.form['phone_number'],
                request.form['location']
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
                request.form['name'],
                request.form['email'],
                request.form['password']
            )

            organization.save()

    return render_template('organizations/apply.html',
                           form = form)

@app.route('/organizations/dashboard/')
@login_required
def organizations_dashboard():
    return render_template('organizations/dashboard.html')

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
