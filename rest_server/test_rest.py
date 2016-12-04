import rest

def main():
	#rest.post('texts', {'from':'121241242'})
	#print rest.get('db')
	#print rest.get('texts/1')
	#rest.delete('texts/1')
	#rest.delete('texts/2')
	#rest.delete('texts/3')
	print rest.get('db')
	rest.put('texts/5', {'from':'hahaha'})
	print rest.get('texts', {'id':4, 'id':5})
	print rest.get('db')

if __name__ == "__main__":
        main()
