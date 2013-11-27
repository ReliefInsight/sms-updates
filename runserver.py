import relief_insight.login

from relief_insight import app
from relief_insight.helpers import is_prod

app.run(debug = not is_prod())
