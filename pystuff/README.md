# some terminology

ROOT: path on hard drive where the files you want to compress/upload live

COMPRESSION_PATH: path on hard drive where tiny-pic can store compressed images. recommended to use `~/desktop/compression`

UPLOAD_DIR: path on hard drive where tiny-pic will move original files that collaborators have requested for you to upload

MAPFILE: file that stores mappings from path->perceptual hash. this is useful for speeding up uploading/reverse image search but NOT necessary.

HOSTNAME: url of tiny-pic website, where compressed images are uploaded to

NAME: choose a name you want to upload as. not important, but good for organizational purposes

SKIP_OPT: skip options are as follows

0. do not skip, recompute hash, recompress, and re-upload
1. if hash and compressed file are present, upload the compressed file but do not recompress
2. if hash and compressed file present, do nothing

# compressing and uploading

`python hash.py ROOT COMPRESSION_PATH NAME SKIP_OPT`


# reverse image search

using hashes of images requested, tiny-pic searches uploaders' hard drives for original files to upload

__short way__

`python locator.py COMPRESSION_PATH`

__long way__

`python locator_long.py ROOT` will search root for phashes by recomputing each image/video's hash


## perceptual hash

uses the ImageHash library. for videos, perceptual hash is the phash of the videos first frame

