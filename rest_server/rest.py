import requests
URL = 'http://localhost:3000/'
def get(query, params_data=None):
	r = requests.get(URL + query, params=params_data) if params_data is not None else requests.get(URL + query)
	r.raise_for_status()
	return r.json()

def post(query, data):
	r = requests.post(URL + query, json = data)
	r.raise_for_status()

def put(query, data):
        r = requests.put(URL + query, json = data)
	r.raise_for_status()

def patch(query, data):
        r = requests.patch(URL + query, json = data)
        r.raise_for_status()

def delete(query):
	r = requests.delete(URL + query)
	r.raise_for_status()

