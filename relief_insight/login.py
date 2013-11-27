from flask.ext.login import LoginManager, login_user

from relief_insight import app
from relief_insight.models import Organization

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
