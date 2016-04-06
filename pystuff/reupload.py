import sys
import os
from os import listdir
from os.path import isfile, join
import requests

import hash as hasher
import config

if __name__=='__main__':
	ROOT = sys.argv[1]
	OUTDIR = config.COMP
	paths = hasher.get_photo_and_video_paths(ROOT)
	mappings = hasher.load_mappings()
	for path in paths:
		print path
		hash = hasher.get_hash(path)
		print 'sending'
		r = hasher.send_to_server(path, hash, OUTDIR)
		print r

ffmpeg -y -i input.mp4 -preset fast -b:v 75k -r 12 -vf scale="200:trunc(ow/a/2)*2" -b:a 3k output.mp4