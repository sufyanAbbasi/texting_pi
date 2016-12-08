import sys, logging
sys.path.insert(0, './secret')
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from auth import *
from datetime import date
from datetime import datetime

client = TwilioRestClient(account_sid, auth_token)

def send_message(message, to_num):
	try:
		client.messages.create(
			to=str(to_num), 
			from_="+14242420412",
			body=str(message.encode('utf-8')), 
		)
	except TwilioRestException as e:
    		logging.error(e)

def get_messages():
	try:
		return client.messages.list(
			#date_sent=date.today(),
			page_size=1000,
			to="+14242420412",
		)
	except TwilioRestException as e:
                logging.error(e)

def get_all_messages():
	try:
                return client.messages.list(
                        #date_sent=date.today(),
                        page_size=1000,
                        #to="+14242420412",
                )
        except TwilioRestException as e:
                logging.error(e)
def get_unprocessed_messages(last_processed_time):
	return [x for x in get_messages() if x.date_sent >= last_processed_time]

def delete_message(message):
	try:
        	client.messages.delete(message.sid)
	except TwilioRestException as e:
                logging.error(e)

def delete_messages_before(when):
	for message in [x for x in get_messages() if x.date_sent < when]:
		delete_message(message)

def delete_all_messages():
	for message in get_all_messages():
                delete_message(message)
