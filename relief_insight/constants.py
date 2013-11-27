import os

SMS_FORMAT = ','.join([
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
