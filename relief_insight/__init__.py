import os

from flask import Flask

app = Flask(__name__)

environment = os.environ.get('RELIEF_INSIGHT_ENVIRONMENT', 'Development')

app.config.from_object('relief_insight.config.{environment}Config'.format(
    environment = environment
))

import relief_insight.views
