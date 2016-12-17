from messages import get_unprocessed_messages, delete_message, send_message
from user import process_text
import os,time, logging, traceback
import cPickle as pickle
from datetime import datetime 
logging.basicConfig(filename='error.log',level=logging.ERROR)

pickle_filepath = "./secret/last_processed_time.p"

def process_unprocessed_texts():
	if not os.path.exists(pickle_filepath):
		last_unprocessed_time = datetime.now()
		pickle.dump({'last_unprocessed_time': last_unprocessed_time}, open(pickle_filepath, 'wb'))
	else:
		last_unprocessed_time = pickle.load(open(pickle_filepath, 'rb'))['last_unprocessed_time']

	unprocessed_messages = get_unprocessed_messages(last_unprocessed_time)
	pickle.dump({'last_unprocessed_time': datetime.now()}, open(pickle_filepath, 'wb'))
	
	numbers_processed = set()
	for message in reversed(unprocessed_messages):
		if message.from_ not in numbers_processed:
			try:
				process_text(message)
			except Exception as e:
				send_message("Yo, something went wrong. Check the error files.", "+14085208922")
				send_message("Sorry, about that. You discovered a bug in my system and I'll have it fixed soon. I'll leave a message in your inbox (text messages). Thanks for baring with me!", message.from_)
				logging.error(datetime.now().strftime("%B %d, %Y %I:%M:%S %p"))
				logging.error(traceback.format_exc())
		numbers_processed.add(message.from_)
		delete_message(message)
	time.sleep(5)

while True:
	process_unprocessed_texts()

