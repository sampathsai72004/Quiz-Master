from flask import Flask, jsonify, request
import logging
import os
from controllers.config import Config
from models.models import db, Subject, Chapter
from controllers.routes import routes_bp
from flask import render_template

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
os.makedirs(os.path.join(app.instance_path), exist_ok=True)
db.init_app(app)
app.register_blueprint(routes_bp)

@app.errorhandler(500)
def internal_error(error):
    logger.error("Server Error: %s", error)
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)