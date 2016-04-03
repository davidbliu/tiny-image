import os, sys
from time import sleep
import press
import requests
from os import listdir
from os.path import isfile, join

def get_requested(hostname, email):
	r = requests.get(
		hostname+'/requested_paths',
		params = {
		'email': email
		})
	return r.json()
	
def update_requested(hostname, email):
		requested = get_requested(hostname, email)
		req_path = os.path.join(ROOT, 'requested')
		try:
				os.mkdir(req_path)
		except:
				pass
		for path in requested:
				os.system('cp '+path+' '+os.path.join(req_path))
		# remove unrequested stuff from requested dir
		fnames = [f for f in listdir(req_path)]
		requested = [x.split('/')[-1] for x in requested]
		removed = [x for x in fnames if x not in requested]
		for r in removed:
				os.system('rm '+os.path.join(req_path, r))
		

if __name__=='__main__':
	ROOT = sys.argv[1]
	EMAIL = sys.argv[2]
	HOSTNAME = 'http://localhost:3000'
	print 'Syncing your images'
	i=0
	while True:
		sleep(0.5)
		print i
		i+=1
		press.compress_and_upload(ROOT, EMAIL, HOSTNAME)
		update_requested(HOSTNAME, EMAIL)
