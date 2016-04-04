import sys
import os
from os import listdir
from os.path import isfile, join
import requests

video_extensions = ['.mp4', '.MOV', '.MP4']
photo_extensions =  ['.jpg', '.png', '.JPG', '.PNG']
valid_extensions = video_extensions + photo_extensions 

def post_file(hostname, compressed_path, original_path, root, email):
	album = '/'.join(original_path.replace(root, '').split('/')[:-1])
	requests.post(
		hostname+'/upload_compressed', 
		files = {'file': open(compressed_path, 'rb')}, 
		params = {
			'email':email,
			'original_path':original_path,
			'album': album})

def is_photo_path(path):
	if path[-4:] in photo_extensions:
		return True
	return False

def needs_compression(original_path, root):
	COMP = os.path.join(root, 'comp')
	if not is_photo_path(original_path):
		opath = original_path.split('/')[-1][:-4]+'_comp.mp4'
	else:
		opath = original_path.split('/')[-1][:-4]+'_comp.png'
	compressed_path = os.path.join(COMP, opath)
	if os.path.isfile(compressed_path):
		return False
	return True

def get_compressed_path(original_path, root):
	COMP = os.path.join(root, 'comp')
	if not is_photo_path(original_path):
		return os.path.join(COMP, original_path.split('/')[-1][:-4]+'_comp.mp4')
	else:
		return os.path.join(COMP, original_path.split('/')[-1][:-4]+'_comp.png')
def compress_video(original_path, root):
	compressed_path = get_compressed_path(original_path, root)
	os.system('ffmpeg -v 0 -n -i '+original_path+' -vf scale=50:-1 -r 3 -an '+compressed_path)
	return compressed_path
def compress_photo(original_path, root):
	compressed_path = get_compressed_path(original_path, root)
	os.system('ffmpeg -v 0 -n -i '+original_path+' -vf scale=200:-1 '+compressed_path)
	return compressed_path

def compress_and_upload(root, email, hostname):
	try:
		os.mkdir(os.path.join(root, 'comp'))
	except:
		pass
	file_paths = []
	for path, subdirs, files in os.walk(root):
		for name in files:
			original_path = os.path.join(path, name)
			file_paths.append(original_path)
	# compress all files
	file_paths = [p for p in file_paths if p[-4:] in valid_extensions and '/comp' not in p]
	i=1
	for original_path in file_paths:
		i+=1
		print str(i) + ' of '+str(len(file_paths))
		if needs_compression(original_path, root):
			print 'compressing file '+str(i)+' of '+str(len(file_paths))+' | '+original_path
			if is_photo_path(original_path):
				compressed_path = compress_photo(original_path, root)
			else:
				compressed_path = compress_video(original_path, root)
			# send compressed file to server
			post_file(hostname, compressed_path, original_path, root, email)

		else:
			# send keepalive to server
			post_file(hostname, get_compressed_path(original_path, root), original_path, root, email)
	

