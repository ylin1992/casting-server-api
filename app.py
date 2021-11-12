from database.models import db, setup_db
from flask import Flask
from flask_cors import CORS
from view.movies import movies_route
from view.actors import actors_route
# --------------------------
# initailize app
# --------------------------
app = Flask(__name__)
setup_db(app)
CORS(app)
app.register_blueprint(movies_route, url_prefix='/movies')
app.register_blueprint(actors_route, url_prefix='/actors')
if __name__ == '__main__':
    app.run(debug=True)