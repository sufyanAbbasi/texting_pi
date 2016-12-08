import color, colortoserver, hashtocolor, command
def process_text(text_data):
	from_num = text_data.from_
	body = text_data.body
	date_sent = text_data.date_sent
	text_data = {'from':from_num, 'body':body,'date_sent':date_sent}
	try:
		color = hashtocolor.get_color(from_num)
	except ValueError:
		generate_new_user(text_data)
	command.process_next_command(color, text_data)	
		
def generate_new_user(text_data):
	new_color = color.generate_random_color()
	while not colortoserver.available_color(new_color):
		new_color = color.generate_random_color()
	hashtocolor.add_hash_color(text_data['from'], new_color)
	colortoserver.new_color(new_color)
	command.init_command(new_color, text_data, "INIT")

def delete(color, data):
        colortoserver.delete_color(color)
        hashtocolor.delete_hash(data['from'])
