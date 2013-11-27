import bcrypt
import md5

from relief_insight.helpers import is_prod
from peewee import *

if is_prod():
    database = None
else:
    database = SqliteDatabase('db.db')

class BaseModel(Model):
    class Meta:
        database = database

class Organization(BaseModel):
    name = CharField()
    email = CharField(unique = True)
    password = CharField()
    approved = BooleanField(default=False)

    @staticmethod
    def new(name, email, password):
        return Organization.create(
            name = name,
            email = email,
            password = bcrypt.hashpw(password, bcrypt.gensalt())
        )

    @staticmethod
    def authenticate(email, password):
        organization = Organization.get(
            Organization.email == email,
            Organization.approved == True
        )

        if bcrypt.hashpw(password, organization.password) == organization.password:
            return organization
        else:
            return None

    def get_auth_token(self):
        return md5.new(self.email + self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.approved

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Location(BaseModel):
    country = CharField()
    state = CharField()
    city = CharField()

    @staticmethod
    def get_choices():
        return [(location.id, location.get_name()) for location in Location.select()]

    def get_name(self):
        return u'%s, %s (%s)' % (self.city, self.state, self.country)

    def get_short_name(self):
        return u'%s, %s' % (self.city, self.state)

class Recipient(BaseModel):
    phone_number = CharField()
    location = ForeignKeyField(Location)

    @staticmethod
    def new(phone_number, location_id):
        return Recipient(
            phone_number = phone_number,
            location = Location.get(Location.id == location_id)
        )
