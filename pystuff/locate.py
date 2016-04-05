import sys
import os
from os import listdir
from os.path import isfile, join
import requests

from PIL import Image
import imagehash

if __name__ == '__main__':
	print 'locating hashes'