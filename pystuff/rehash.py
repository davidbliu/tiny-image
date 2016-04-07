import sys
from PIL import Image
import requests
import os
from os import listdir
from os.path import isfile, join
import config
import hash as hasher


try:
	root = sys.argv[1]
except:
	root = False

if root:
	paths = []
	for path, subdirs, files in os.walk(root):
		for name in files:
			original_path = os.path.join(path, name)
			if hasher.is_photo_or_video_path(original_path) and not hasher.is_comp_path(original_path):
				paths.append(original_path)
				
	with open(config.HASHLOG, 'a') as hashlog:
		for i in range(len(paths)):
			path = paths[i]
			if hasher.is_photo_path(path):
				hash = hasher.get_photo_hash(path)
			else:
				hash = hasher.get_video_hash(path)
	                hasher.write_hash_log(path, str(hash))
			print str(path)+':'+str(hash)
else:
	# compress log
	mappings = hasher.load_mappings()
	with open(config.HASHLOG, 'wb') as hashlog:
		for key in mappings:
			hashlog.write(key+':'+mappings[key]+'\n')
