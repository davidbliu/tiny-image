from flask import Flask, request, render_template, send_from_directory
app = Flask(__name__, static_url_path='/static')
import os
import hash as hasher

@app.route("/")
def hello():
	directories = os.listdir('/Volumes')
	directories += os.listdir('.')
	return render_template('index.html', name = 'david', directories = directories)

@app.route('/run_compressor', methods = ['POST'])
def run_compressor():
	print 'running compressor'
	os.system('python hash.py "." skip send')
	return 'running compressor'

@app.route('/get_hash_log')
def get_hash_log():
	mappings = hasher.load_mappings()
	return str(mappings)

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js', path)

if __name__ == "__main__":
		app.run(debug=True)
