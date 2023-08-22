#!/usr/bin/python3
"""
connection with flask
"""


from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def storage_close(exception):
    """storage close"""
    storage.close()


if __name__ == "__main__":
    hosting = os.getenv("HBNB_API_HOST", "0.0.0.0")
    porting = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=hosting, port=porting, threaded=True)