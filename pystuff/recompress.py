import sys
from PIL import Image
import requests
import os
from os import listdir
from os.path import isfile, join
import config
import hash as hasher

root = sys.argv[1]

paths = []
for path, subdirs, files in os.walk(root):
	for name in files:
		original_path = os.path.join(path, name)
		if hasher.is_photo_or_video_path(original_path) and not hasher.is_comp_path(original_path):
			paths.append(original_path)

mappings = hasher.load_mappings()

with open(config.HASHLOG, 'a') as hashlog:
	for i in range(len(paths)):
		path = paths[i]
		if path in mappings.keys():
			hash = mappings[path]
		elif hasher.is_photo_path(path):
			hash = hasher.get_photo_hash(path)
		else:
			hash = hasher.get_video_hash(path)
		compressed_path = os.path.join(config.COMP, hash)
		print 'removing '+compressed_path
		os.system('rm '+compressed_path+'*')
		print 'removed '+path
