import sys
import os
from os import listdir
from os.path import isfile, join
import requests

from PIL import Image
import imagehash
import pickle
import config
import ffmpeg_helpers

video_extensions = ['.mp4', '.MOV', '.MP4', '.mov']
photo_extensions =  ['.jpg', '.png', '.JPG', '.PNG']
valid_extensions = video_extensions + photo_extensions 

is_photo_path = lambda x: x[-4:] in photo_extensions
is_video_path = lambda x: x[-4:] in video_extensions
is_photo_or_video_path = lambda x: is_video_path(x) or is_photo_path(x)
is_comp_path = lambda x: '/'+config.COMP in x

def needs_compressing(path, compressed_path): 
	if not isfile(compressed_path):
		return True
	if is_video_path(path):
		if ffmpeg_helpers.is_corrupted(compressed_path):
			return True
		size = ffmpeg_helpers.get_filesize_kb(compressed_path)
		print '\tcompressed_size: '+str(size)
		if  size >= 2000:
			return True
		original_duration = ffmpeg_helpers.get_video_length(path)
		compressed_duration = ffmpeg_helpers.get_video_length(path)
		print '\tdurations (orig, comp): '+str([original_duration, compressed_duration])
		frac = abs(compressed_duration-original_duration)/original_duration
		if frac > 0.1:
			return True
	return False

def write_hash_log(path, hash):
	with open(config.HASHLOG, 'a') as hashlog:
		hashlog.write(path+':'+hash+'\n')

def load_mappings():
	mappings = {}
	if not isfile(config.HASHLOG):
		os.system('touch '+config.HASHLOG)
	with open(config.HASHLOG, 'rb') as hashlog:
		for line in hashlog:
			path, hash = [str(x).strip() for x in line.split(':')]
			mappings[path] = hash
	return mappings

def get_video_hash(path):
	os.system('ffmpeg -v 0 -ss 0 -i "'+path+'" -s 320x240 -frames:v 1 -y output.png')
	hash = imagehash.phash(Image.open('output.png'))
	os.system('rm output.png')
	return str(hash)

get_photo_hash = lambda path: str(imagehash.phash(Image.open(path)))

def get_hash(path):
	if is_photo_path(path):
		return get_photo_hash(path)
	else:
		return get_video_hash(path)

def compress_photo(path, compressed_path):
	os.system('ffmpeg -v 0 -y -i "'+path+'" -vf scale=200:-1 '+compressed_path)

def compress_video(path, compressed_path):
	osize = os.path.getsize(path)
	osize_mb = osize / 1000000 # size in megabytes
	temp_path = config.TEMP+config.VIDEO_SUFFIX
	length_seconds = ffmpeg_helpers.get_video_length(path)
	bitrate = min(128, int(float(config.VID_SIZE)*8192/float(length_seconds)))
	bitrate = str(bitrate)+'k'
	print '\tlength of video is '+str(length_seconds)+' seconds'
	print '\tbitrate: '+bitrate
	print '\tcompressing '+str(osize_mb)+' MB'
	os.system('ffmpeg -v error -y -i "'+path+'" -r 10 -b:v '+bitrate+' -vf scale="-1:200" -b:a 3k '+temp_path)
	print '\tcopying temp.mp4 to '+compressed_path
	os.system('cp temp.mp4 '+compressed_path)
	print '\tfinal size: '+str(os.path.getsize(compressed_path)/1000)+' KB'

def get_photo_and_video_paths(root):
	original_paths = []
	for path, subdirs, files in os.walk(root):
		for name in files:
			original_path = os.path.join(path, name)
			if is_photo_or_video_path(original_path) and not is_comp_path(original_path):
				original_paths.append(original_path)
	return original_paths

def compress_directory(root):
	mappings = load_mappings()
	original_paths = get_photo_and_video_paths(root)
	print 'found '+str(len(original_paths))+' files to compress'
	sys.stdout.flush()
	sent_hashes = get_sent_hashes()
	for i in range(len(original_paths)):
		path = original_paths[i]
		if SKIP_VID and is_video_path(path) or path.split('/')[-1][0]=='.':
			i = i+1
			continue
		print 'file '+str(i+1)+' of '+str(len(original_paths))+ ' | '+path
		if path not in mappings.keys():
			hash = get_hash(path)
			write_hash_log(path, hash)
		else:
			hash = mappings[path]
		suffix = config.PHOTO_SUFFIX if is_photo_path(path) else config.VIDEO_SUFFIX
		compressed_path = os.path.join(config.COMP, hash + suffix)
		if needs_compressing(path, compressed_path) or not SKIP:
			print '\tcompressing...'
			if is_photo_path(path):
				compress_photo(path, compressed_path)
			else:
				compress_video(path, compressed_path)
		else:
			print '\tskipped compression'

		if hash in sent_hashes:
			print '\t'+hash+' is already sent'
		if SEND and (hash not in sent_hashes or RESEND):
			print '\tsending to server...'
			r = send_to_server(path, compressed_path)
			print '\tresponse: '+str(r)
			sys.stdout.flush()

def get_sent_hashes():
	return requests.get(config.HOSTNAME +'/photos/hashes').json()

def send_to_server(path, compressed_path):
	hash = compressed_path.split('/')[-1].split('.')[0]
	album = path.replace(path.split('/')[-1], '')
	r = requests.post(HOSTNAME+'/upload_photo',
		files = {'file': open(compressed_path, 'rb')},
		params = {
			'email': EMAIL,
			'album': album,
			'hash': hash,
			'original_path': path,
			'original_size':ffmpeg_helpers.get_filesize_mb(path),
			'compressed_size':ffmpeg_helpers.get_filesize_kb(compressed_path)})
	return r

HOSTNAME = config.HOSTNAME
EMAIL = config.EMAIL
SEND = False
SKIP = False
SKIP_VID = False
RESEND = False
if __name__=='__main__':
	email = config.EMAIL
	SKIP = 'skip' in sys.argv
	SEND = 'send' in sys.argv
	SKIP_VID = 'skip_vid' in sys.argv
	RESENT = 'resent' in sys.argv
	print 'skip: '+str(SKIP)
	print 'send to '+HOSTNAME+': '+str(SEND)

	os.system('mkdir '+config.COMP)
	print '1. re-creating '+config.COMP
	print '2. compressing files into '+config.COMP
	compress_directory(sys.argv[1])
