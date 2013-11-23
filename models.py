from peewee import *

class Organization(Model):
    name = CharField()
    email = CharField()
    password = CharField()

class Location(Model):
    country = CharField()
    city = CharField()

    def get_name(self):
        return u'%s (%s)' % (city, country)

    @staticmethod
    def get_choices():
        return []
        # return [(location.id, location.get_name()) for location in Location.select()]

class Recipient(Model):
    phone_number = CharField()
    location = ForeignKeyField(Location)
