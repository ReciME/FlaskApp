from flask import Flask
import threading, csv, tempfile, gzip, shutil, tarfile, os, sqlite3, argparse, subprocess, traceback, sys, io, zipfile, urllib, ssl, datetime, math
from flask import send_file, Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

application = app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY ='lht+)8on!@s)dw!ikizr=59h=4f8x=vziupnpnv-h=8fh)ki*g',
    CURR_RECIPE = None,
    TYPES = ["Produce", "Can", "Pasta", "Meat", "Spice", "Dairy", "Other"],
    MEASUREMENTS = ["Ounces", "Pounds", "Quantity", "Table Spoon", "Tea Spoon", "Cups"],
    PICS = 'static/utils/pictures',
    USERID = '1',
    DOCS = 'static/utils/documents'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Add database configurations which are set in
# the EBS environment
if ('RDS_HOSTNAME' in os.environ):
    app.config.update(dict(
        ENGINE='mysql',
        NAME=os.environ['RDS_DB_NAME'],
        USER=os.environ['RDS_USERNAME'],
        PASSWORD=os.environ['RDS_PASSWORD'],
        HOST=os.environ['RDS_HOSTNAME'],
        PORT=os.environ['RDS_PORT'],
    ))
else:
    # This means we are in local development and so all database
    # information should be in a file called db.csv
    dbDict = {}
    with open('db.csv', 'r') as csvfile:
        dbReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in dbReader:
            dbDict[row[0]] = row[1]
    app.config.update(dict(
        ENGINE='mysql',
        NAME=dbDict['NAME'],
        USER=dbDict['USER'],
        PASSWORD=dbDict['PASSWORD'],
        HOST=dbDict['HOST'],
        PORT=dbDict['PORT'],
    ))

# The database string for connecting to the database
dbString = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    app.config['USER'],
    app.config['PASSWORD'],
    app.config['HOST'],
    app.config['PORT'],
    app.config['NAME']
)

app.config['SQLALCHEMY_DATABASE_URI'] = dbString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#This will essentially tell flask where the first url route '/' is located.
from views import *
from api import *

if __name__ == "__main__":
    app.run()
