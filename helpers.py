import os

def is_prod():
    return os.environ.has_key('RELIEF_INSIGHT_PRODUCTION')

