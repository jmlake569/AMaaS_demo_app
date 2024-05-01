from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
import json
import secrets
import logging
from logging.handlers import RotatingFileHandler
import argparse
import amaas.grpc
import time

UPLOAD_FOLDER = '/app/uploads'
LOG_FILE = '/app/logs/app.log'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = secrets.token_hex(32)

# Setup logging to log to both file and console
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=3)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Define the allowed_file function to allow all file types
def allowed_file(filename):
    return True  # Allow all file types

# Function to scan uploaded file
import time

# Function to scan uploaded file
def scan_uploaded_file(file_path, handle):
    try:
        s = time.perf_counter()

        # Call scan_file without named arguments for handle
        result = amaas.grpc.scan_file(handle, file_path)
        elapsed = time.perf_counter() - s
        logger.info(f"Scanning completed in {elapsed:0.2f} seconds.")
        logger.info(f"Scanning complete: {result}")
        return result
    except Exception as e:
        logger.error("Error during scanning:", exc_info=True)
        return None



@app.route('/', methods=['GET'])
def root():
    # Redirect to the login page when accessing the root URL
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('upload_file'))
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            logger.warning("Upload attempt with no file part in request.")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            logger.warning("Upload attempt without selecting a file.")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            logger.info(f"File saved: {file_path}")

            # Initialize args with default values
            args = argparse.Namespace(
                api_key=os.environ.get('API_KEY'),
                region=os.environ.get('REGION')
            )

            # Initiate the AMaaS connection
            handle = amaas.grpc.init_by_region(api_key=args.api_key, region=args.region)
            logger.debug("AMaaS connection initialized.")

            scan_result = scan_uploaded_file(file_path, handle)

            if scan_result is not None:
                scan_result_dict = json.loads(scan_result)
                scan_result_code = scan_result_dict.get('scanResult', -1)
                logger.info(f"Scan result code: {scan_result_code}")

                if scan_result_code == 1:
                    amaas.grpc.quit(handle)
                    logger.info("File is malicious, disconnecting.")
                    return render_template('scan_results.html', scan_result_code=1, scan_results=scan_result_dict)
                
                logger.info(f"Scan result: {scan_result}")
                amaas.grpc.quit(handle)
                logger.info("File scan completed and connection closed.")
                return render_template('scan_results.html', scan_message="File uploaded successfully.", scan_result_code=0)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
