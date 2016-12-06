import messages, colortoserver, hashtocolor
from datetime import datetime
from dateutil import tz

def error(message, data):
	messages.send_message(message, data['from'])

def init_command(color, data, command_name):
	sys_commands[command_name]['init'](color, data)

def reset_commands(color):
	colortoserver.update_color(color, {'commands':[]})

def process_command(color, data, command):
	try:
		sys_commands[command['command']]['process'](color, data)
	except RuntimeError:
		reset_commands(color)
		error("Sorry, something went wrong on my part. Please reenter your command or help for a list of commands", data)

def check_command(color, check_val):
	commands = colortoserver.get_color(color)['commands']
        command = commands.pop()
	if command['command'] != check_val:
                raise RuntimeError('Incorrect Command')
	colortoserver.update_color(color, {'commands':commands})
	return command

def get_user_command(data):
	return data['body'].lower().strip().split()[0] if data['body'].lower().strip().split()[0] in user_commands else False

def get_user_command_rest(data):
	return data['body'].lower().strip().split()[1::]

def process_next_command(color, data):
	commands = colortoserver.get_color(color)['commands']
	if len(commands):
		process_command(color, data, commands[-1])
	elif get_user_command(data):
		process_user_command(color, data)
	else:
		error("I didn't quite catch that. Text help for a list of commands.", data)

def process_user_command(color, data, user_command=None):
	user_command = get_user_command(data) if not user_command else user_command
	for sys_command in user_commands[user_command]['commands']:
		init_command(color, data, sys_command)

def init_validate(color, data):
	colortoserver.new_command(color, "VALIDATE")
	messages.send_message('Reply Yes or No (or Yup, Yep, Yiss, Nope...):', data['from'])

affirmation = {
'yes':True,
'no': False,
'yup':True,
'yep':True,
'nope':False,
'yiss':True,
}
def validate(color, data):
	command = check_command(color, 'VALIDATE')
	answer = data['body']
	try:
		validation = affirmation[answer.lower()]
	except KeyError:
		error("Sorry, I didn't get that. I'll consider it a no.", data)
		validation = False
	data['validation']=validation
	process_next_command(color, data)

def init_init(color, data):
	colortoserver.new_command(color, "INIT")
	messages.send_message("Welcome! You're new here, by my records. Would you like to be a part of this thing? If you reply no, I will forget your existence until you text me again.", data['from'])
	init_command(color, data, "VALIDATE")

def initialize(color, data):
	command = check_command(color, 'INIT')
	try:
		validation = data['validation']
	except KeyError:
		raise RuntimeError('No Validation Command')
	if validation:
		messages.send_message("Sweet! Welcome to the team. Text help to see a list of commands.", data['from'])
	else:
		messages.send_message("All good. Text me any time.", data['from'])
		delete(color, data)

def init_delete(color, data):
	messages.send_message("Thanks for being a part of this! You will be deleted from this server, but you can always text back at this number.\nHowever, everything you've posted will remain on the server.", data['from'])	
	delete(color, data)

def delete(color, data):
	colortoserver.delete_color(color)
	hashtocolor.delete_hash(data['from'])
	messages.send_message('You are now completely deleted from this server.', data['from'])

def init_help(color, data):
	secondary_command = get_user_command_rest(data)
	if not secondary_command:
		commands_list = []
		for key in user_commands:
			commands_list.append("- {0}:  {1}".format(key, user_commands[key]['text']))
		commands_string = '\n'.join(commands_list)  
		messages.send_message("Here are all the currently available commands:\n{0}".format(commands_string), data['from'])
	elif secondary_command[0] in user_commands:
		messages.send_message(user_commands[secondary_command[0]]['help'], data['from'])		
	else:
		messages.send_message("No further help options for this command. Text help for a list of commands.", data['from'])
def init_color(color, data):
	hex_color = hex(color)
	message = "Your color in hex is #{0}.\nSee your color at: colorhexa.com/{0}".format(hex_color[2:])
	messages.send_message(message, data['from'])

def init_scavenger_hunt(color, data):
	message = scavenger_hunt_dict[data['from']]['init']
	colortoserver.new_command(color, "SCAVENGER")
	messages.send_message(message, data['from'])
	process_next_command(color, data)

def scavenger_hunt(color,data):
	clues = scavenger_hunt_dict[data['from']]['clues']
	command = check_command(color, 'SCAVENGER')
	clue_index = command['command_state']
	if clue_index >= len(clues):
		messages.send_message(scavenger_hunt_dict[data['from']]['finish'], data['from'])
		return
	clue = clues[clue_index]
	in_progress = command['in_progress']
	if not in_progress:
		messages.send_message(clue['text'], data['from'])
		colortoserver.new_command(color, "SCAVENGER", {'command_state':clue_index, 'in_progress': 1})
	else: 
		if data['body'].lower().strip() == 'hint':
                        messages.send_message(clue['hint'], data['from'])
			colortoserver.new_command(color, "SCAVENGER", {'command_state':clue_index, 'in_progress': 1})
		elif data['body'].lower().strip() == 'repeat':
			messages.send_message(clue['text'], data['from'])
			colortoserver.new_command(color, "SCAVENGER", {'command_state':clue_index, 'in_progress': 1})
		elif data['body'].lower().strip() == clue['validation']:
			clue_index += 1
			colortoserver.new_command(color, "SCAVENGER", {'command_state':clue_index, 'in_progress': 1})
			process_next_command(color,data)
		else:
			messages.send_message('Nope! Try again. Text hint for help or repeat to repeat the clue', data['from'])
			colortoserver.new_command(color, "SCAVENGER", {'command_state':clue_index, 'in_progress': 1})

def init_upc(color, data):
	secondary_commands = get_user_command_rest(data)
	if not secondary_commands:
		today_upc = colortoserver.get_today_upc()
		if not today_upc:
			 messages.send_message('No submissions yet for today, be the first to text in today!\nText help upc for a list of upc commands.', data['from'])
		else:
			last_submitted = today_upc[-1];
			hex_color = '#'+ hex(last_submitted['color'])[2:]
			timestamp = datetime.fromtimestamp(last_submitted['date_sent']).strftime("%B %d, %Y %I:%M:%S %p")
			upc_str = 'From {0} at {1},\n there are {2} people in the UPC line'.format(hex_color, timestamp, last_submitted['value'])
			if 'message' in last_submitted:
				upc_str += ' and left the message:\n{0}'.format(last_submitted['message'])
			messages.send_message(upc_str, data['from'])
	else:
		try:	
			num_submitted = int(secondary_commands[0])
    		except ValueError:
        		messages.send_message("Sorry, the value you submitted was not a number. Text help upc for how to submit upc responses.", data['from'])
			return
		upc_message = " ".join(secondary_commands[1::])
		colortoserver.update_upc(color, num_submitted, {'message':upc_message} if upc_message else {})
		messages.send_message("Thank you! Your submission was submitted. To make sure, text upc to see your message (unless someone updated over you).", data['from'])

def init_about(color, data):
	messages.send_message("Thanks for your curiosity. This is an open-source project by Sufyan Abbasi (github.com/sufyanAbbasi/texting_pi) where every user is a hexadecimal color. All of the web services used can only be accessed on Vassar wifi. I'm all about privacy so that's why I don't save anyone's phone number and instead I use an encryption algorithm to match you up with your color. I'm interested in creating a social network that uses simple messaging so anyone with a cell phone can be a part of it. Enjoy!", data['from'])

def null_command(color, data):
	pass
sys_commands = {
	"VALIDATE": {
			'init':init_validate,
			'process':validate,
		    },
	"INIT":     {
			'init':init_init,
			'process':initialize,
		    },
	"DELETE":   {
			'init':init_delete,
			'process':delete,
		    },
	"HELP":     {
			'init':init_help,
			'process':null_command,
		    },
	"COLOR":    {
			'init':init_color,
			'process':null_command,
		    },
	"SCAVENGER":{
			'init':init_scavenger_hunt,
			'process':scavenger_hunt,
		    },
	"UPC":	{
			'init':init_upc,
			'process':null_command,
		},
	"ABOUT":{
			'init':init_about,
			'process':null_command,
		},	
}


user_commands = {
	'help': {
			'text': 'lists available commands. You can use help <command> to get more help options.',
			'help': 'uses:\nhelp help\n  - Yep, help help does give you help on how to use help. Help!',
			'commands' : ['HELP'],
		},
	'delete':{
			'text': 'deletes your user color from the server, but everything you submitted will remain.',
			'help': 'uses:\ndelete\n  - You will be removed from the server until you text us back.',
			'commands': ['DELETE'],
		},
	'reset':{
			'text': 'resets your account with a new color',
			'help': "uses:\nreset\n  - Deletes then reinitializes you as if you were never here. Isn't it nice?",
			'commands':['DELETE', 'INIT'],
		},
	'color':{
			'text': 'tells you what your color hex value is',
			'help': "uses:\ncolor\n  - Texts you back what your color is and link to a website that shows you your color.",
			'commands' : ['COLOR']
		},
	'upc':	{
			'text': 'report or see last reported UPC Line',
			'help': 'uses:\nupc\n  - States the last reported UPC line and when it was reported.'
				+ '\n\nupc <number>\n  - Reports the value to the server'
				+ '\n\nupc <number> <message>\n  - Reports the value to the server and leave a message about what ingredients are left',
			'commands' : ['UPC'],
		},
	'about':{
			'text': 'tells you about this project!',
			'help': 'uses:\nabout\n - tells you what this projects about.',
			'commands' : ['ABOUT'],
		},
}
