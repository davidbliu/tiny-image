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

requested_hashes = requests.get(config.HOSTNAME+'/hashes').json()

found = []
for i in range(len(paths)):
	path = paths[i]
	print 'searched '+str(i)+' of '+str(len(paths))
	if hasher.is_photo_path(path):
		hash = hasher.get_photo_hash(path)
	else:
		hash = hasher.get_video_hash(path)
	if hash in requested_hashes:
		print '\tfound '+path
		found.append(path)

print 'these paths were found'
for path in found:
	print path