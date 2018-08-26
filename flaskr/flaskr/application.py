from flask import Flask
import threading, csv, tempfile, gzip, shutil, tarfile, os, sqlite3, argparse, subprocess, traceback, sys, io, zipfile, urllib, ssl, datetime, math
from flask import send_file, Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

application = app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app = Flask(__name__)
app.config.from_object(__name__)
ALLOWED_EXTENSIONS = set(['pcap'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
db = SQLAlchemy(app)
ROOT = ""
app.config.update(dict(
    SECRET_KEY ='lht+)8on!@s)dw!ikizr=59h=4f8x=vziupnpnv-h=8fh)ki*g',
    PICS = ROOT + "/static/pictures",
    CURR_RECIPE = None,
    TYPES = ["Produce", "Can", "Pasta", "Meat", "Spice", "Dairy", "Other"],
    MEASUREMENTS = ["Ounces", "Pounds", "Quantity", "Table Spoon", "Tea Spoon", "Cups"],
    DOCS = ROOT + "/documents"
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#This will essentially tell flask where the first url route '/' is located.
from views import *

if __name__ == "__main__":
    app.run()
