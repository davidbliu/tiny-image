import sys
import os
from os import listdir
from os.path import isfile, join
import requests

from PIL import Image
import imagehash

video_extensions = ['.mp4', '.MOV', '.MP4', '.mov']
photo_extensions =  ['.jpg', '.png', '.JPG', '.PNG']
valid_extensions = video_extensions + photo_extensions 
COMP = 'comp'

is_photo_path = lambda x: x[-4:] in photo_extensions
is_video_path = lambda x: x[-4:] in video_extensions
is_photo_or_video_path = lambda x: is_video_path(x) or is_photo_path(x)
is_comp_path = lambda x: '/'+COMP in x


def get_video_hash(video_path):
	os.system('ffmpeg -v 0 -ss 0 -i '+video_path+' -s 320x240 -frames:v 1 -y output.png')
	hash = imagehash.phash(Image.open('output.png'))
	os.system('rm output.png')
	return hash

def compress_photo(path, outdir):
	hash = imagehash.phash(Image.open(path))
	compressed_path = os.path.join(outdir, str(hash)+'.png')
	os.system('ffmpeg -v 0 -n -i '+path+' -vf scale=200:-1 '+compressed_path)
	return hash

def compress_video(path, outdir):
	hash = get_video_hash(path)
	compressed_path = os.path.join(outdir, str(hash)+'.webm')
	os.system('ffmpeg -v 0 -n -i '+path+' -vf scale=130:-1 -r 3 -an '+compressed_path)
	return hash

def compress_directory(root, outdir):
	original_paths = []
	for path, subdirs, files in os.walk(root):
			for name in files:
				original_path = os.path.join(path, name)
				if is_photo_or_video_path(original_path) and not is_comp_path(original_path):
					original_paths.append(original_path)
	for i in range(len(original_paths)):
		path = original_paths[i]
		print 'compressing '+str(i)+' of '+str(len(original_paths))+ ' | '+path.split('/')[-1]
		if is_photo_path(path):
			h = compress_photo(path, outdir)
		else:
			h = compress_video(path, outdir)
		send_to_server(path, h, outdir)

def send_to_server(path, hash, outdir):
	album = path.replace(path.split('/')[-1], '')
	suffix = '.png' if is_photo_path(path) else '.mp4'
	compressed_path = os.path.join(outdir, str(hash)+suffix)
	print compressed_path
	requests.post(HOSTNAME+'/upload_photo',
		files = {'file': open(compressed_path, 'rb')},
		params = {'email': 'default', 'album': album, 'hash': hash, 'filename': str(hash)+suffix})

HOSTNAME = 'http://localhost:3000'
if __name__=='__main__':
	ROOT = sys.argv[1]
	OUTDIR = os.path.join(ROOT, COMP)
	os.system('rm -rf '+OUTDIR)
	os.system('mkdir '+OUTDIR)
	print '1. re-creating '+OUTDIR
	print '2. compressing files into '+OUTDIR
	compress_directory(ROOT, OUTDIR)
