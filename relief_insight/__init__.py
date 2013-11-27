from flask import Flask
from helpers import is_prod

app = Flask(__name__)

# app configuration
if is_prod():
    app.secret_key = os.environ['RELIEF_INSIGHT_SECRET_KEY']
else:
    app.secret_key = 'ruf4biun4fib4iu2i3u42398rhuibe'

import relief_insight.views
