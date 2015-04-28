from flask import Flask, request, Response
from flask_jwt import JWT
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="")

app.config.from_object('gb.settings')
db = SQLAlchemy(app)
session = db.session
jwt = JWT(app)
app.url_map.strict_slashes = False

import gb.models
import gb.controllers