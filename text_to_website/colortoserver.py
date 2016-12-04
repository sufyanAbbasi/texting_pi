import sys
sys.path.insert(0, './../rest_server')

import rest, time
from copy import deepcopy
from color import validate_color

color_factory = {
	'color'        : None,
	'date_created' : None,
	'authenticated': 0,
	'texts'        : [],
	'responses'    : [],
	'commands'     : [],
	'has_commands' : 0,
	'has_texts'    : 0,
	'has_responses': 0,
}

text_factory = {
	'body'      : None,
	'date_sent' : None,
	'processed' : 0,
}

response_factory = {
	'from'      : None,
	'body'      : None,
	'date_sent' : None,
	'processed' : 0,
}

command_factory = {
	'command'      : None, 
	'date_sent'    : None,
	'command_state': 0,
	'in_progress'  : 0,
	'finished'     : 0,
}

def new_object(factory, data):
	obj = deepcopy(factory)
	for key in data:
		obj[key] = data[key]
	return obj

def new_color(color):
	data = {}
	if validate_color(color) and available_color(color):
		data['color'] = color
		data['date_created'] = time.time()
	else:
		raise ValueError(hex(color) + ' is not a valid color or it is not available')
	new_color = new_object(color_factory, data)
	rest.post('colors', new_color)

def get_id(color):
	try:
		return rest.get('colors',{'color':color})[0]['id']
	except IndexError:
		raise ValueError("invalid color")

def available_color(color):
	try:
		get_id(color)
		return False
	except ValueError:
		return True

def update_color(color, data):
	id = get_id(color)
	rest.patch('colors/{0}'.format(id), data)

def get_color(color):
        try:
                return rest.get('colors',{'color':color})[0]
        except IndexError:
                raise ValueError("invalid color")

def delete_color(color):
	id = get_id(color)
	rest.delete('colors/{0}'.format(id))

def new_command(color, command_name, data={}):
	data['command'] = command_name
	data['date_sent'] = time.time()
	new_command = new_object(command_factory, data)
	commands = get_color(color)['commands']
	commands.append(new_command)
	update_color(color, {'commands':commands})

