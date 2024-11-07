# main.py

import os
from flask import Flask, request, redirect, url_for, render_template
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Use absolute path

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

print("Upload Folder Path:", app.config['UPLOAD_FOLDER'])  # Debugging output

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML form

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No image uploaded", 400  # Return an error if no image is found

    image_file = request.files['image']
    if image_file:
        # Generate a unique filename
        base_filename = 'captured_image'
        extension = '.png'
        filename = base_filename + extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if the file already exists and increment the filename
        counter = 1
        while os.path.exists(file_path):
            filename = f"{base_filename}_{counter}{extension}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1

        # Save the uploaded file
        image_file.save(file_path)
        print(f"Saved image as: {filename}")  # Debugging output
        return redirect(url_for('index'))
    
    return "No image found", 400  # Return an error if no image is found

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Specify port 5001