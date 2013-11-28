from twilio.rest import TwilioRestClient

from relief_insight import app
from relief_insight.models import Location

def send_text_messages(sms_data):
    client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

    message_body = app.config['SMS_FORMAT'].format(
        location = sms_data['location'],
        water = sms_data['water'],
        medicine = sms_data['medicine'],
        food = sms_data['food'],
        clothing = sms_data['clothing'],
        eta = sms_data['eta']
    )

    for phone_number in sms_data['phone_numbers']:
        message = client.messages.create(
            to = phone_number,
            from_ = app.config['TWILIO_NUMBER'],
            body = message_body
        )

def get_sms_data_from_form(form):
    location = Location.get(
        Location.id == form.location.data
    )

    phone_numbers = [
        recipient.phone_number for recipient in location.recipient_set
    ]

    return {
        'location': location.get_short_name(),
        'phone_numbers': phone_numbers,
        'water': form.water.data,
        'medicine': form.medicine.data,
        'food': form.food.data,
        'clothing': form.clothing.data,
        'eta': form.eta.data
    }
