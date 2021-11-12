from database.models import db, setup_db
from flask import Flask
from flask_cors import CORS

# --------------------------
# initailize app
# --------------------------
app = Flask(__name__)
setup_db(app)
CORS(app)