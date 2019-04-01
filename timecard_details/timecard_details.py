from urllib import request

from django.contrib.messages.storage import session

from DRApp import settings


class Timecard_details(object):
    def __init__(self):
        self.session = request.session
        # GET timecarddetails FROM SESSION OBJECT
        timecarddetails = self.session.get(settings.TIMECARDDETAILS_SESSION_ID)
        #  IF timecarddetails DOES NOT EXIST IN SESSION , CREATE NEW
        if not timecarddetails:
            self.session[settings.TIMECARDDETAILS_SESSION_ID] = {}
            timecarddetails =  self.session[settings.TIMECARDDETAILS_SESSION_ID]

        self.timecarddetails = timecarddetails

    def save(self):
        self.session[settings.TIMECARDDETAILS_SESSION_ID] = self.timecarddetails

    def clear(self):
        self.session[settings.TIMECARDDETAILS_SESSION_ID]={}

    def get_labor_total(self):

    def get_machine_total(self):

    def get_timecard_total(self):
