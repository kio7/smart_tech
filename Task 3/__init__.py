import os
from flask import request, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
from PIL import Image

from baseconfig import app

# Define the upload folder and allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the route to the main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was submitted
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    # Check if the file has a valid name and extension
    if file.filename == '':
        return "No selected file"

    if not allowed_file(file.filename):
        return "Invalid file extension"

    if file:
        # Securely save the uploaded file
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Convert the uploaded image to JPEG
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f"{os.path.splitext(filename)[0]}.jpg"  # Use the same filename but with a .jpg extension
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        try:
            img = Image.open(input_path)
            img.convert('RGB').save(output_path, 'JPEG')
        except Exception as e:
            return f"Error converting file: {str(e)}"

        # Provide a success message and a download link for the converted file
        success_message = f'File uploaded successfully. <a href="/download/{output_filename}">Download Converted File</a>'
        return success_message


# Define a route to download the converted file
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
