import hash as hasher
import sys
if __name__ =='__main__':
	# path = sys.argv[1]
	path = '/Volumes/My Passport for Mac/Wesley 3rd Gen/MVI_9430.MOV'
	# path = '/Users/davidbliu/desktop/GOPR0875.mp4'
	# hasher.compress_video(path, '.')
	from Tkinter import Tk
	from tkFileDialog import askopenfilename

	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	print(filename)