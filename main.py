from flask import Flask, request, send_from_directory
import os
import zipfile

app = Flask(__name__)

# Define the directory for storing uploaded and unzipped files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UNZIP_FOLDER = 'unzipped'
app.config['UNZIP_FOLDER'] = UNZIP_FOLDER

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file provided"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        unzip_file(file.filename)
        return "File uploaded and unzipped successfully"

# Function to unzip the uploaded file
# Performace can be improved
def unzip_file(filename):
    with zipfile.ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(app.config['UNZIP_FOLDER'], filename.split('.')[0]))

# Route to download unzipped files
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UNZIP_FOLDER'], filename)

# Status request
@app.route('/status/<action_id>', method=['GET'])
def status(action_id):
    action = get_action()
    return {'action': action.action, 'complete': action.complete, 'progress': action.progress}

if __name__ == '__main__':
    app.run(debug=True)
