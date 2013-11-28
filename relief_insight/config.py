import os

from peewee import SqliteDatabase

class Config:
    SECRET_KEY = os.environ['RELIEF_INSIGHT_SECRET_KEY']

    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    TWILIO_NUMBER = os.environ['TWILIO_PHONE_NUMBER']

    SMS_FORMAT = ','.join([
        'Loc:{location}',
        'Water:{water}',
        'Meds:{medicine}',
        'Food:{food}',
        'Clothes:{clothing}',
        'ETA:{eta}'
    ])

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = SqliteDatabase('db.db')

class ProducionConfig(Config):
    DEBUG = False 
    DATABASE = None
