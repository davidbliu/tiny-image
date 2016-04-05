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


if __name__ == '__main__':
	map = hasher.load_mappings()
	if not map.keys():
		print 'no hash_log'
	else:
		map = {v: k for k, v in map.items()}
		print 'pulling hashes from '+config.HOSTNAME
		hashes = get_requested_hashes()
		paths = []
                found = [h for h in hashes if h in map.keys()]
                print 'found '+str(len(found)) + ' of '+str(len(hashes))
                paths = [map[h] for h in found]
		upload_dir = 'upload_these'
		os.system('rm -rf "'+upload_dir+'"')
		os.system('mkdir "'+upload_dir+'"')
		for path in paths:
			os.system('cp "'+path+'" '+upload_dir)
		print 'opening finder'
		from subprocess import call
		call(["open", upload_dir])

