from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sys
from urllib2 import urlopen

BASE_URL = "http://www.emergencyclosingcenter.com/ecc/home.jsp"

html = urlopen(BASE_URL).read()
soup = BeautifulSoup(html)

for table in soup.findAll('table'):
    if table.parent.name == 'td':
        data = table

closings = []
count = 0
table_rows = data.findAll('tr')

if table_rows[1].text.strip() == "No facilities have reported.":
    print "No closings today."
    sys.exit()

for tr in table_rows:
    school_name = tr.findAll('td')[1].text.strip()
    city = tr.findAll('td')[3].text.strip()
    status = tr.findAll('td')[5].text.strip()
    if status.find("TODAY") != -1:
        status_date = datetime.now()
        status_date = status_date.strftime("%Y-%m-%d")
    elif status.find("TOMORROW") != -1:
        status_date = datetime.now()
        status_date = status_date + timedelta(days=+1)
        status_date = status_date.strftime("%Y-%m-%d")
    else:
        status_date = None

    if school_name == "":
        school_name = closings[count - 1]['school_name']
        city = closings[count - 1]['city']
    
    if school_name != "Facility Name":
        closings.append({'school_name': school_name,
                         'city': city,
                         'status': status,
                         'status_date': status_date})     
        count = count + 1

for closing in closings:
    print "%s: %s - %s [%s]" % (closing['school_name'], closing['city'], closing['status'], closing['status_date'])
