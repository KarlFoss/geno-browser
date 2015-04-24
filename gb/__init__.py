import os
import json

from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="")

app.config.from_object('gb.settings')
db = SQLAlchemy(app)
session = db.session
auth = HTTPBasicAuth()
app.url_map.strict_slashes = False

import gb.models
import gb.controllers
