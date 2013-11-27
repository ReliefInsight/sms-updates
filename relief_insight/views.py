from flask import request, render_template, redirect, flash, url_for
from flask.ext.login import logout_user, login_required, current_user

from relief_insight import app
from relief_insight.models import Organization, Location, Recipient
from relief_insight.forms import ApplyOrganizationForm, LoginOrganizationForm, SignUpRecipientForm, SendTextForm
from relief_insight.login import login_organization
from relief_insight.helpers import send_text_messages, get_sms_data_from_form

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
            send_text_messages(get_sms_data_from_form(form))
            flash('Your message was successfully sent!')

    return render_template('organizations/dashboard.html',
                           form = form)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
