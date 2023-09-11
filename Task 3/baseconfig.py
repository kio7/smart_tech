from flask import Flask
import sys, os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(sys.path[0]) + "/uploads"