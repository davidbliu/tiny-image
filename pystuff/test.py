import hash as hasher
import sys
if __name__ =='__main__':
	path = sys.argv[1]
	type = sys.argv[2]
	if type == 'hash':
		print 'start hash'
		print hasher.get_photo_hash(path)
		print hasher.compress_photo(path, '.')
	if type == 'compress':
		print 'start compress'