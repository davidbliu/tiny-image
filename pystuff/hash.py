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

def needs_compressing(path, hash, outdir): 
	if is_photo_path(path):
		cpath = hash+config.PHOTO_SUFFIX
	else:
		cpath = hash+config.VIDEO_SUFFIX
	if cpath in os.listdir(outdir):
		return False
	return True

def needs_hashing(path, mappings):
	return path in mappings.keys()

def write_hash_log(path, hash):
	with open(config.HASHLOG, 'a') as hashlog:
		hashlog.write(path+':'+hash+'\n')

def load_mappings():
	mappings = {}
	with open(config.HASHLOG, 'rb') as hashlog:
		for line in hashlog:
			path, hash = [str(x).strip() for x in line.split(':')]
			mappings[path] = hash
	return mappings

def get_video_hash(video_path):
	os.system('ffmpeg -v 0 -ss 0 -i "'+video_path+'" -s 320x240 -frames:v 1 -y output.png')
	hash = imagehash.phash(Image.open('output.png'))
	os.system('rm output.png')
	return str(hash)

get_photo_hash = lambda path: str(imagehash.phash(Image.open(path)))

def compress_photo(path, hash, outdir):
	compressed_path = os.path.join(outdir, str(hash)+config.PHOTO_SUFFIX)
	os.system('ffmpeg -v 0 -y -i "'+path+'" -vf scale=200:-1 '+compressed_path)
	return hash

def compress_video(path, hash, outdir):
	compressed_path = os.path.join(outdir, str(hash)+config.VIDEO_SUFFIX)
	# os.system('ffmpeg -i "'+path+'" -vf scale=420:-1 -r 3 -ab 3k '+compressed_path)
	os.system('ffmpeg -v 0 -y -i "'+path+'" -preset fast -b:v 150k -vf scale="300:trunc(ow/a/2)*2" -b:a 3k '+compressed_path)#output_file.mp4')#+compressed_path)
	return hash

def compress_directory(root, outdir, skip = True):
	mappings = load_mappings()
	original_paths = []
	for path, subdirs, files in os.walk(root):
			for name in files:
				original_path = os.path.join(path, name)
				if is_photo_or_video_path(original_path) and not is_comp_path(original_path):
					original_paths.append(original_path)
	print 'found '+str(len(original_paths))+' files to compress'
	sys.stdout.flush()
	for i in range(len(original_paths)):
		path = original_paths[i]
		if path not in mappings.keys():
			if is_photo_path(path):
				hash = get_photo_hash(path)
			else:
				hash = get_video_hash(path)
			write_hash_log(path, hash)
		else:
			hash = mappings[path]
		if needs_compressing(path, hash, outdir) or not skip:
			print 'compressing '+str(i)+' of '+str(len(original_paths))+ ' | '+path
			if is_photo_path(path):
				compress_photo(path, hash, outdir)
			else:
				compress_video(path, hash, outdir)
		else:
			print 'skipping | '+str(i)+' of '+str(len(original_paths))+ ' | '+path
		
		print '\tsending to server'
		r = send_to_server(path, hash, outdir)
		print '\tresponse: '+str(r)
			# r = send_to_server(path, mappings[path], outdir)
			# print '\tresponse: '+str(r)
		sys.stdout.flush()

def send_to_server(path, hash, outdir):
	album = path.replace(path.split('/')[-1], '')
	suffix = config.PHOTO_SUFFIX if is_photo_path(path) else config.VIDEO_SUFFIX
	compressed_path = os.path.join(outdir, str(hash)+suffix)
	r = requests.post(HOSTNAME+'/upload_photo',
		files = {'file': open(compressed_path, 'rb')},
		params = {'email': EMAIL, 'album': album, 'hash': hash})
	return r

HOSTNAME = config.HOSTNAME
MAPFILE = config.MAPFILE
EMAIL = config.EMAIL
COMP = config.COMP
if __name__=='__main__':
	ROOT = sys.argv[1]
	OUTDIR = config.COMP
	email = config.COMP
	SKIP = sys.argv[2] in ['True', 'true']

	os.system('mkdir '+OUTDIR)
	print '1. re-creating '+OUTDIR
	print '2. compressing files into '+OUTDIR
	compress_directory(ROOT, OUTDIR, SKIP)
