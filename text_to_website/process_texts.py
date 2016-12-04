from messages import get_unprocessed_messages
from user import process_text
import os,time
import cPickle as pickle
from datetime import datetime 

pickle_filepath = "./secret/last_processed_time.p"

def process_unprocessed_texts():
	if not os.path.exists(pickle_filepath):
		last_unprocessed_time = datetime.now()
		pickle.dump({'last_unprocessed_time': last_unprocessed_time}, open(pickle_filepath, 'wb'))
	else:
		last_unprocessed_time = pickle.load(open(pickle_filepath, 'rb'))['last_unprocessed_time']

	unprocessed_messages = get_unprocessed_messages(last_unprocessed_time)
	pickle.dump({'last_unprocessed_time': datetime.now()}, open(pickle_filepath, 'wb'))

	for message in reversed(unprocessed_messages):
		process_text(message)
	
	time.sleep(5)

while True:
        process_unprocessed_texts()

