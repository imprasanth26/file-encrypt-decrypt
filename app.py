import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime
from encryption import encrypt_file, decrypt_file

app = Flask(__name__)
UPLOAD_FOLDER = os.getcwd()  # Save in root directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['encryptionDB']
log_collection = db['logs']

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        file = request.files.get('file')
        action = request.form.get('action')

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)  # Save the uploaded file in root

            try:
                if action == 'encrypt':
                    encrypt_file(filepath)
                else:
                    decrypt_file(filepath)

                log_collection.insert_one({
                    "filename": filename,
                    "action": action,
                    "timestamp": datetime.now()
                })

                message = f"✅ {filename} has been successfully {action}ed and overwritten."
            except Exception as e:
                message = f"⚠️ Error: {str(e)}"
        else:
            message = "❌ No file selected."

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

