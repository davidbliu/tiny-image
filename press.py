import sys
import os
from os import listdir
from os.path import isfile, join
import requests

EMAIL = 'alice.sun94@gmail.com'
video_extensions = ['.mp4', '.MOV', '.MP4']
image_extensions =  ['.jpg', '.png']
valid_extensions = video_extensions + image_extensions 

def post_file(filename, original_path):
	requests.post(
		'http://localhost:3000/upload_compressed', 
		files = {'file': open(filename, 'rb')}, 
		params = {
			'email':EMAIL,
			'original_path':original_path})

if __name__ == '__main__':
	root = sys.argv[1]
	os.system('mkdir comp')
	videos = []
	images = []
	for path, subdirs, files in os.walk(root):
		for name in files:
			fname = os.path.join(path, name)
			if fname[-4:] in video_extensions:
				videos.append(os.path.join(path, name))
			if fname[-4:] in image_extensions:
				images.append(os.path.join(path, name))

	i=0 
	for video in videos:
		i+=1
		print 'video '+str(i)+' of '+str(len(videos))
		compressed_path = 'comp/' + video.split('/')[-1][:-4]+'_comp.mp4'
		os.system('ffmpeg -v 0 -n -i '+video+' -vf scale=100:-1 -r 3 -an '+compressed_path)
		post_file(compressed_path, video)

	i=0
	for image in images:
		i+=1
		print 'image '+str(i)+' of '+str(len(images))
		compressed_path = 'comp/'+image.split('/')[-1][:-4]+'_comp.png'
		os.system('ffmpeg -v 0 -n -i '+image+' -vf scale=300:-1 '+compressed_path)
		post_file(compressed_path, image)
	

