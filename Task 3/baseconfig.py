from flask import Flask
import sys, os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/uploads"
app.config['DOWNLOAD_FOLDER'] = "/download"