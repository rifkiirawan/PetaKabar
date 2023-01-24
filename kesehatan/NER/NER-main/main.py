# ['kamis (9/6/2022)', 'selasa (7/6)', 'rabu (8/6)']
# ['rabu (20/4/2022)', 'selasa (19/4/2022)']
import re
import time
import datetime
from datetime import datetime as dt

def getNewsTime(dateTime: str):
    month_to_number = {
      'jan': '1',
      'feb': '2',
      'mar': '3',
      'apr': '4',
      'mei': '5',
      'jun': '6',
      'jul': '7',
      'agu': '8',
      'sep': '9',
      'okt': '10',
      'nov': '11',
      'des': '12',
    }

    splitted_timestamp = dateTime.split()
    pre_formatted_time = splitted_timestamp[1] + '/' + month_to_number[splitted_timestamp[2].lower()] + '/' + splitted_timestamp[3]
    
    return pre_formatted_time

def compareDateArray(sortByLength):
    year = None
    timestampList = []
    
    def convertToTimestapms(date):
        return int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()))

    for i, tempTime in enumerate(sortByLength):
        # Find the content inside parentheses
        currTime = re.search(r'\((.*?)\)', tempTime)
        
        if (currTime != None):
            currTime = currTime.group(1)
            
        currTime = str(currTime)
        
        if (tempTime.lower() == 'kemarin'):
            timestampList.append(convertToTimestapms(newsDate) - (24*60*60))
        
        if (currTime != None):
            # Find the year
            splitted = currTime.split('/')
            formattedDate = None
            if (len(splitted) == 3):
                year = splitted[2]
                timestampList.append(convertToTimestapms(currTime))
            elif (len(splitted) == 2):
                formattedDate = (splitted[0] + '/' + splitted[1] + '/' + year)
                timestampList.append(convertToTimestapms(formattedDate))
    
    return dt.fromtimestamp(sorted(timestampList)[0]).strftime('%d/%m/%Y')
# ------------------------------------------------------------------------- #

# ------------------------------------------------------------------------- #
times = ['rabu (8/6)', 'kamis (9/6/2022)', 'selasa (7/6)', 'kemarin']
sortedTimes = sorted(times, key=len, reverse=True)

# Tanggal berita diformat gini
newsDate = getNewsTime('Selasa, 5 Jun 2022 06:30 WIB')

# if array is empty return news date
if(len(sortedTimes) == 0):
    print(newsDate)
# if array not empty and not contain kemarin
elif (len(sortedTimes) > 1):
    print(compareDateArray(sortedTimes))
