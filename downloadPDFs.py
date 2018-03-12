#Downloads last 60 days of HUPD Daily Crime Logs
#Stephen Moon for the Harvard College Open Data Project

from urllib.request import urlopen
from datetime import datetime, timedelta
import os

downloadedDates = []

def getDates():
    now = datetime.now()
    dates = []
    #starting with yesterday, because today's isn't available yet
    for i in range(1, 60):
        dates.append(now - timedelta(days = i))

    return formatDates(dates)

def formatDates(dates):
    formatted = []
    for date in dates:
        month = date.month
        day = date.day
        year = date.year % 100
        if date.month < 10:
            month = "0%d" % month
        if date.day < 10:
            day = "0%d" % day
        #dates are in format MMDDYY
        dateStr = "%s%s%s" % (month, day, year)
        formatted.append(dateStr)
    return formatted

#returns a tuple: first value is date (MMDDYY) and second is link
def getLinks(dateStrings):
    links = []
    for date in dateStrings:
        link = "https://www.hupd.harvard.edu/files/hupd/files/%s.pdf" % date
        links.append((date, link))
    return links

def downloadFiles():
    dates = getDates()
    files = os.listdir("data/")
    newDates = []
    for date in dates:
        if "%s.pdf" % (date) not in files:
            newDates.append(date)
    links = getLinks(newDates)
    for link in links:
        downloadFile(link)

    return downloadedDates

def downloadFile(link):
    try:
        response = urlopen(link[1])
        file = open("data/%s.pdf" % link[0], 'wb')
        file.write(response.read())
        file.close()
        downloadedDates.append(link[0])
    except IOError:
        #if the file is missing, not much we can do about it
        x = 2
