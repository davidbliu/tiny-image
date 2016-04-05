import sys
import os
from os import listdir
from os.path import isfile, join
import requests

from PIL import Image
import imagehash

import config
import hash as hasher


def get_requested_hashes():
	r = requests.get(config.HOSTNAME + '/hashes')
	return [str(x) for x in r.json()]

def get_mappings():
	m = {}
	with open('hash_log', 'rb') as hashlog:
		for line in hashlog:
			path, hash = line.split(':')
			hash = hash.strip()
			m[hash] = path
	return m

if __name__ == '__main__':
	# OUTDIR = sys.argv[1]
	map = get_mappings() # hasher.load_mappings(OUTDIR)
	# map = {v: k for k, v in map.items()}
	if not map.keys():
		# print 'no mapfile found in your compression folder'
		print 'no hash_log'
	else:
		print map.keys()
		print 'pulling hashes from '+config.HOSTNAME
		hashes = get_requested_hashes()
		paths = []
		for hash in hashes:
			if hash in map.keys():
				print 'found: '+hash
				paths.append(map[hash])
			else:
				print 'not found: '+hash
		upload_dir = 'upload_these' #os.path.join(OUTDIR, config.UPLOAD)
		os.system('rm -rf "'+upload_dir+'"')
		os.system('mkdir "'+upload_dir+'"')
		for path in paths:
			os.system('cp "'+path+'" '+upload_dir)

