from flask import Flask
import os

template_dir = os.path.abspath("templates")


app = Flask(__name__, template_folder=template_dir)
app.secret_key = "your-secret-key"


from app import routes