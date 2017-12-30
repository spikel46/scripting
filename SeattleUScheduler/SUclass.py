from __future__ import print_function
import os, time, sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SUID = os.environ["SU_USER"]
SU_pass = os.environ["SU_PASS"]

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



browser = "Chrome"

loginBtn = "//li[@id='acctLogin']"
userInput = "//input[@id='USER_NAME']"
passInput = "//input[@id='CURR_PWD']"
studentOption = "//div[contains(@id,'mainMenu')]//a[contains(.,'Students')][not(contains(., 'Prospective'))]"
manageClassOption = "//span[contains(.,'Manage Classes')]/parent::a"

classRows = "//td[contains(@class,'CSVIEW')]/parent::tr"

dateRegex = "\d{2}/\d{2}/\d{2}"
dayRegex = "([A-z]*day)"
timeRegex = "\d{2}:\d{2}[A|P]M"
roomRegex = "[A-z]*, RM .*"

def convertDateTimes(times, startDate):
    """
    'start': {
      'dateTime': '2015-05-28T09:00:00-07:00',
      'timeZone': 'America/Los_Angeles',
    },
    'end': {
      'dateTime': '2015-05-28T17:00:00-07:00',
    """
    pacificTimeOffset = "-07:00"
    dateArray = startDate.split("/")
    eventDate="20"+dateArray[2]+"-"+dateArray[0]+"-"+dateArray[1]
    startDateTime=eventDate+"T"+(times[0])+":00"+pacificTimeOffset
    endDateTime=eventDate+"T"+(times[1])+":00"+pacificTimeOffset
    return (startDateTime,endDateTime)

def createRRule(endDate, days):
    #RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20150919T063000Z
    rrule = "RRULE:FREQ=WEEKLY;"
    repeatDays = "BYDAY="
    until="UNTIL=20"
    #MO,TU,WE,TH,FR,SA,SU
    if "Monday" in days:
        repeatDays += "MO,"
    if "Tuesday" in days:
        repeatDays += "TU,"
    if "Wednesday" in days:
        repeatDays += "WE,"
    if "Thursday" in days:
        repeatDays += "TH,"
    if "Friday" in days:
        repeatDays += "FR,"
    if "Saturday" in days:
        repeatDays += "SA,"
    if "Sunday" in days:
        repeatDays += "SU,"

    #remove ending comma and add semicolon for until argument
    repeatDays = repeatDays[0:-1]+';'
    #print(repeatDays)

    #split date by slashes[MM,DD,YY]
    dateArray = endDate.split('/')
    until+=dateArray[2]
    until+=(dateArray[0]+dateArray[1]+'T235900Z')
    #print(until)

    return rrule+repeatDays+until

def convertTime(time):
    #print("Before: ",time)
    if time[-2:] == "AM":
        if(time == "12:00AM"):
            time = "00:00AM"
    elif time[-2:] == "PM":
        if(time[:2] != "12"):
            newTime = int(time[:2])+12
            time = str(newTime) + time[2:]
    time = time[:-2]
    #print("After: ", time)
    return time


def convertTimes(times):
    timeArray = []
    for time in times:
        timeArray.append(convertTime(time))

    #print("Time Array: ", timeArray)
    return timeArray

def parseMeetingInfo(meetingString):
    date = re.findall(dateRegex,meetingString)
    days = re.findall(dayRegex,meetingString)
    time = re.findall(timeRegex,meetingString)

    #print(time)
    time = convertTimes(time)
    #print(time)
    time = convertDateTimes(time,date[0])
    #print(time)

    rrule = createRRule(date[1],days)
    startTime=time[0]
    endTime=time[1]
    room = re.findall(roomRegex,meetingString)[0]

    """
    print("Date: ", date)
    print("Days: ", days)
    print("Time: ", time)
    print("Room: ", room)
    """
    #add argument here for how many classes there are (lab + lecture)
    return (rrule,startTime,endTime,room)

def getDriver(choice):
    if(choice == "Mozilla"):
        return webdriver.Firefox()
    elif(choice == "Chrome"):
        return webdriver.Chrome()
    else:
        console.log("Invalid Option")
        return null;

def main():
    """
    Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    driver = getDriver(browser)
    driver.get("https://suonline.seattleu.edu")

    #wait?
    time.sleep(3)
    driver.find_element_by_xpath(loginBtn).click()

    time.sleep(4)
    driver.find_element_by_xpath(userInput).send_keys(SUID)
    driver.find_element_by_xpath(passInput).send_keys(SU_pass+Keys.ENTER)

    time.sleep(3)
    driver.find_element_by_xpath(studentOption).click()

    time.sleep(3)
    driver.find_element_by_xpath(manageClassOption).click()

    time.sleep(3)
    classes = driver.find_elements_by_xpath(classRows)

    for row in classes:
        cTitle=row.find_element_by_xpath(".//td[contains(@class,'SHORT_TITLE')]").text
        cInfo=row.find_element_by_xpath(".//td[contains(@class,'MEETING_INFO')]").text
        cTeacher="Class with: " + row.find_element_by_xpath(".//td[contains(@class,'FACULTY_INFO')]").text
        #maybe check for semicolon in meeting info instead?
        try:
            meetingInfo = parseMeetingInfo(cInfo)
            if ';' in meetingInfo:
                print("Two Classes")
            #https://developers.google.com/google-apps/calendar/v3/reference/events/insert#examples
            #https://eduardopereira.pt/2012/06/google-calendar-api-v3-set-color-color-chart/
            #use argument here to create/add 2 new events
            classJson = {
              'summary': cTitle,
              'location': meetingInfo[3],
              'description': cTeacher,
              'start': {
                'dateTime': meetingInfo[1],
                'timeZone': 'America/Los_Angeles',
              },
              'end': {
                'dateTime': meetingInfo[2],
                'timeZone': 'America/Los_Angeles',
              },
              'recurrence': [
                meetingInfo[0]
              ],
              'colorId' : '11',
              'attendees': [],
              'reminders': {
                'useDefault': False,
                'overrides': [
                  {'method': 'popup', 'minutes': 30},
                  {'method': 'popup', 'minutes': 10},
                ],
              },
            }
            #print(classJson)
            classJson = service.events().insert(calendarId='primary', body=classJson).execute()
            print('Event created: %s' % (classJson.get('htmlLink')))
        except:
            print("skip " + cTitle + " " +cInfo)



if __name__ == '__main__':
    main()
