import pickle, encrypt

def add_hash_color(from_num, color):
	hashmap = pickle.load( open( "./secret/hash-color.p", "rb" ) )
	last_digits = from_num[-4:]
	if last_digits not in hashmap:
		hashmap[last_digits] = {}
	hashmap[last_digits][encrypt.generate_hash(from_num)]=color
	pickle.dump(hashmap, open( "./secret/hash-color.p", "wb" ))

def set_hash_color(from_num, color):
        hashmap = pickle.load( open( "./secret/hash-color.p", "rb" ) )
        last_digits = from_num[-4:]
        if last_digits not in hashmap:
		raise ValueError("number not in hash")
	for hash in hashmap[last_digits]:
		if encrypt.verify_password(from_num, hash):
			hashmap[last_digits][hash] = color 
        		pickle.dump(hashmap, open( "./secret/hash-color.p", "wb" ))
			return
	raise ValueError("number not in hash")

def get_color(from_num):
        hashmap = pickle.load( open( "./secret/hash-color.p", "rb" ) )
        last_digits = from_num[-4:]
        if last_digits not in hashmap:
                raise ValueError("number not in hash")
        for hash in hashmap[last_digits]:
                if encrypt.verify_password(from_num, hash):
                        return hashmap[last_digits][hash]
        raise ValueError("number not in hash")

def delete_hash(from_num):
	hashmap = pickle.load( open( "./secret/hash-color.p", "rb" ) )
	last_digits = from_num[-4:]
        if last_digits not in hashmap:
                raise ValueError("number not in hash")
        for hash in hashmap[last_digits]:
                if encrypt.verify_password(from_num, hash):
                        hashmap[last_digits].pop(hash, None)
			if not hashmap[last_digits]:
				hashmap.pop(last_digits, None)
			pickle.dump(hashmap, open( "./secret/hash-color.p", "wb" ))
			return
        raise ValueError("number not in hash")


def reset_hash():
	 pickle.dump({}, open( "./secret/hash-color.p", "wb" ))
