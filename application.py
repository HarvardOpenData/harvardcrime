import os
import re
from downloadPDFs import downloadFiles
from urllib.request import urlopen
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue
from geocodeCSV import updateCSV
from scraper import scrapeNew

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

#checks if all the latest logs have been downloaded
def upToDate():
    files = os.listdir("data/")
    yesterday = datetime.now() - timedelta(days = 1)
    month = yesterday.month
    day = yesterday.day
    year = yesterday.year % 100
    if yesterday.month < 10:
        month = "0%d" % month
    if yesterday.day < 10:
        day = "0%d" % day
    dateStr = "%s%s%s.pdf" % (month, day, year)
    if dateStr in files:
        return True
    else:
        return False

@app.route("/")
def index():
    """Render map."""
    #if not os.environ.get("API_KEY"):
    #    raise RuntimeError("API_KEY not set")
    #return render_template("index.html", key=os.environ.get("API_KEY"))
    if upToDate():
        return render_template("index.html")
    else:
        newDates = downloadFiles()
        scrapeNew(newDates)
        updateCSV()
        return render_template("index.html")
