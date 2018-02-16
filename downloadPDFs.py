#Downloads last 60 days of HUPD Daily Crime Logs
#Stephen Moon for the Harvard College Open Data Project

import urllib2
from datetime import datetime, timedelta

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
def getLinks():
    dateStrings = getDates()
    links = []
    for date in dateStrings:
        link = "https://www.hupd.harvard.edu/files/hupd/files/%s.pdf" % date
        links.append((date, link))
    return links

def main():
    links = getLinks()
    for link in links:
        downloadFile(link)

def downloadFile(link):
    try:
        response = urllib2.urlopen(link[1])
        file = open("data/%s.pdf" % link[0], 'wb')
        file.write(response.read())
        file.close()
    except IOError, e:
        #if the file is missing, not much we can do about it

if __name__ == "__main__":
    main()
