from flask import Flask
import sys, os

app = Flask(__name__)
app.config["SECRET_KEY"] = "my super duper safe secret key"