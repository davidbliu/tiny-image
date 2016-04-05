import sys
import os
from os import listdir
from os.path import isfile, join
import requests

from PIL import Image
import imagehash
import pickle
import config

video_extensions = ['.mp4', '.MOV', '.MP4', '.mov']
photo_extensions =  ['.jpg', '.png', '.JPG', '.PNG']
valid_extensions = video_extensions + photo_extensions 
COMP = 'comp'

is_photo_path = lambda x: x[-4:] in photo_extensions
is_video_path = lambda x: x[-4:] in video_extensions
is_photo_or_video_path = lambda x: is_video_path(x) or is_photo_path(x)
is_comp_path = lambda x: '/'+COMP in x

def needs_compressing(path, mappings):
	if path in mappings.keys():
		return False
	return True

def write_mappings(mappings, outdir):
	with open(os.path.join(outdir, MAPFILE), 'wb') as mapfile:
		pickle.dump(mappings, mapfile)

def load_mappings(outdir):
	h = {}
	if os.path.isfile(os.path.join(outdir, MAPFILE)):
		with open(os.path.join(outdir, MAPFILE), 'rb') as mapfile:
			h = pickle.load(mapfile)
	for key in h.keys():
		if is_photo_path(key):
			path = str(h[key]) + '.png'
		else:
			path = str(h[key]) + '.webm'
		path = os.path.join(outdir, path)
		if not os.path.isfile(os.path.join(outdir, path)):
			h.pop(key, None)
	return h

def get_video_hash(video_path):
	os.system('ffmpeg -v 0 -ss 0 -i "'+video_path+'" -s 320x240 -frames:v 1 -y output.png')
	hash = imagehash.phash(Image.open('output.png'))
	os.system('rm output.png')
	return str(hash)

get_photo_hash = lambda path: str(imagehash.phash(Image.open(path)))

def compress_photo(path, outdir):
	hash = get_photo_hash(path)
	compressed_path = os.path.join(outdir, str(hash)+'.png')
	os.system('ffmpeg -v 0 -y -i "'+path+'" -vf scale=200:-1 '+compressed_path)
	return hash

def compress_video(path, outdir):
	print '\tgetting hash'
	hash = get_video_hash(path)
	print '\tcompressing video'
	compressed_path = os.path.join(outdir, str(hash)+'.webm')
	os.system('ffmpeg -v 0 -y -i "'+path+'" -b:v 24k -vf scale=200:-1 -r 10 -ab 3k '+compressed_path)
	return hash

def compress_directory(root, outdir, skip = True):
	mappings = load_mappings(outdir)
	original_paths = []
	for path, subdirs, files in os.walk(root):
			for name in files:
				original_path = os.path.join(path, name)
				if is_photo_or_video_path(original_path) and not is_comp_path(original_path):
					original_paths.append(original_path)
	for i in range(len(original_paths)):
		path = original_paths[i]
		if needs_compressing(path, mappings) or not skip:
			print 'compressing '+str(i)+' of '+str(len(original_paths))+ ' | '+path.split('/')[-1]
			if is_photo_path(path):
				h = compress_photo(path, outdir)
			else:
				h = compress_video(path, outdir)
			print '\tsending to server'
			r = send_to_server(path, h, outdir)
			print '\tresponse: '+str(r)
			mappings[path] = str(h)
			write_mappings(mappings, outdir)
		else:
			print 'skipping | '+path.split('/')[-1]

def send_to_server(path, hash, outdir):
	album = path.replace(path.split('/')[-1], '')
	suffix = '.png' if is_photo_path(path) else '.webm'
	compressed_path = os.path.join(outdir, str(hash)+suffix)
	r = requests.post(HOSTNAME+'/upload_photo',
		files = {'file': open(compressed_path, 'rb')},
		params = {'email': EMAIL, 'album': album, 'hash': hash})
	return r

HOSTNAME = config.HOSTNAME
MAPFILE = config.MAPFILE
EMAIL = config.EMAIL

if __name__=='__main__':
	ROOT = sys.argv[1]
	OUTDIR = sys.argv[2]
	EMAIL = sys.argv[3]
	SKIP = sys.argv[4] in ['True', 'true', '1']

	os.system('mkdir '+OUTDIR)
	print '1. re-creating '+OUTDIR
	print '2. compressing files into '+OUTDIR
	compress_directory(ROOT, OUTDIR, SKIP)
