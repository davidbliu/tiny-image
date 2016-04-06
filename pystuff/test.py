import hash as hasher
import sys, os
if __name__ =='__main__':
	# # path = sys.argv[1]
	# path = '/Volumes/My Passport for Mac/Wesley 3rd Gen/MVI_9430.MOV'
	# # path = '/Users/davidbliu/desktop/GOPR0875.mp4'
	# # hasher.compress_video(path, '.')
	# from Tkinter import Tk
	# from tkFileDialog import askopenfilename

	# Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	# print(filename)
	# path = 'hash.pyc'
	# # path = 'comp/7f8405b9c565d469.mp4'
	# cpaths = os.listdir('comp')
	# paths = []
	# mappings=hasher.load_mappings()
	# for key in mappings.keys():
	# 	if "/Volumes/passport/cabo_david" in key:
	# 		found = [c for c in cpaths if mappings[key] in c]
	# 		paths = paths + found
	# print paths
	# # paths = os.listdir('comp')
	# for i in range(len(paths)):
	# 	print str(i)+' of '+str(len(paths))
	# 	s = hasher.is_corrupted(os.path.join('comp', paths[i]))
	hasher.compress_video('input.mp4', 'some_random_hash', '.')