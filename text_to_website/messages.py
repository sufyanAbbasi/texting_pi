import sys
sys.path.insert(0, './secret')
from twilio.rest import TwilioRestClient
from auth import *
from datetime import date
from datetime import datetime

client = TwilioRestClient(account_sid, auth_token)

def send_message(message, to_num):
	client.messages.create(
		to=str(to_num), 
		from_="+14242420412",
		body=str(message), 
	)

def get_messages():
	return client.messages.list(
		date_sent=date.today(),
		page_size=1000,
	)

def get_unprocessed_messages(last_processed_time):
	return [x for x in get_messages() if x.date_sent >= last_processed_time and x.to == '+14242420412']

def delete_messages():
	for message in get_messages():
		client.messages.delete(message.sid)
