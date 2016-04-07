import subprocess
import re
from decimal import Decimal
import config
import os
 
def get_filesize_mb(path):
    return os.path.getsize(path)/1000000
def get_filesize_kb(path):
    return os.path.getsize(path)/1000
def get_video_length(path):
    process = subprocess.Popen(['ffmpeg',  '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
     
    hours = float(matches['hours'])
    minutes = float(matches['minutes'])
    seconds = float(matches['seconds'])
 
    total = 0
    total += 60 * 60 * hours
    total += 60 * minutes
    total += seconds
    return total

def is_corrupted(path):
    errors = []
    os.system('ffmpeg -v error -i "'+path+'" -f null - 2>'+config.ERROR_LOG)
    with open (config.ERROR_LOG, 'rb') as error_log:
        errors = [line for line in error_log]
    if errors:
        return True
    else:
        return False