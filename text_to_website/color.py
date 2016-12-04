import random, math
def generate_random_color():
	return int(math.floor(random.random()*16777215))

def validate_color(color):
        return color >= 0x000000 and color <= 0xffffff
