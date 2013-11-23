from flask import Flask, request, render_template, redirect, flash, url_for
from forms import *
from models import *

# app
app = Flask(__name__)
app.secret_key = 'ruf4biun4fib4iu2i3u42398rhuibe'

# forms
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = LoginOrganizationForm(request.form)
        if form.validate():
            pass
    else:
        form = LoginOrganizationForm()

    return render_template('index.html', form = form)

@app.route('/recipients/sign-up/', methods=['GET', 'POST'])
def recipients_sign_up():
    if request.method == 'POST':
        form = SignUpRecipientForm(request.form)
        if form.validate():
            pass
    else:
        form = SignUpRecipientForm()

    form.location.choices = Location.get_choices()

    return render_template('recipients/sign-up.html',
                           form = form)

@app.route('/organizations/apply/', methods=['GET', 'POST'])
def organizations_apply():
    if request.method == 'POST':
        form = ApplyOrganizationForm(request.form)
        if form.validate():
            pass
    else:
        form = ApplyOrganizationForm()

    return render_template('organizations/apply.html',
                           form = form)

if __name__ == '__main__':
    app.run(debug=True)
