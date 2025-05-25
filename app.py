from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import hashlib
import requests
from datetime import datetime
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx', 'xlsx', 'png', 'jpg', 'jpeg', 'exe', 'zip'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mock data for demonstration
MOCK_DATA = {
    "file": {
        "status": "malicious",
        "detection": "32/68",
        "filename": "sample.exe",
        "analysis": {
            "sha256": "a1b2c3d4...",
            "file_type": "PE32 executable",
            "size": "2.4 MB",
            "first_seen": "2023-05-10",
            "last_analysis": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "engines": {
            "Microsoft": "malicious",
            "Kaspersky": "malicious", 
            "ESET": "clean",
            "McAfee": "malicious",
            "Symantec": "suspicious"
        }
    },
    "url": {
        "status": "suspicious",
        "detection": "5/72",
        "url": "http://malicious.example.com",
        "analysis": {
            "domain": "example.com",
            "ip": "192.168.1.1",
            "country": "United States",
            "registrar": "Bad Registrar Inc.",
            "last_analysis": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "engines": {
            "Google Safe Browsing": "malicious",
            "Cisco Talos": "clean",
            "Malwarebytes": "malicious"
        }
    }
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan/file', methods=['POST'])
def scan_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # In a real app, you would analyze the file here
        # For demo, we return mock data
        result = MOCK_DATA["file"]
        result["filename"] = filename
        result["analysis"]["size"] = f"{os.path.getsize(filepath)/1024/1024:.2f} MB"
        result["analysis"]["sha256"] = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
        
        return jsonify(result)
    
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/scan/url', methods=['POST'])
def scan_url():
    url = request.form.get('url', '').strip()
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # In a real app, you would analyze the URL here
    # For demo, we return mock data
    result = MOCK_DATA["url"]
    result["url"] = url
    result["analysis"]["domain"] = url.split('//')[-1].split('/')[0]
    
    return jsonify(result)

@app.route('/results')
def results():
    scan_type = request.args.get('type')
    target = request.args.get('target')
    return render_template('results.html', scan_type=scan_type, target=target)

if __name__ == '__main__':
    app.run(debug=True)