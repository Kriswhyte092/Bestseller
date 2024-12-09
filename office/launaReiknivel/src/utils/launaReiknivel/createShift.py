from utils.launaReiknivel.shiftEmployee import Employee
from utils.launaReiknivel.shiftDate import Date
from utils.launaReiknivel.shiftDuration import Duration
from datetime import datetime

class createShift:
    def __init__(self, name, id, date, location, clockIn, clockOut, status):
        self.name = name
        self.id = id
        self.date = date
        self.location = location 
        self.clockIn = clockIn
        self.clockOut = clockOut
        self.status = status

    def getEmployee(self):
        return Employee(self.name, self.id).__str__()

    def getDate(self):
        return Date(self.date).getDate()

    def getLocation(self):
        return self.location

    def getDuration(self):
        if Date(self.date).isWeekend() is True:
            return Duration(self.clockIn, self.clockOut).getDurationWeekEnd()
        return Duration(self.clockIn, self.clockOut).getDurationWeekDay()

    def getStatus(self):
        return self.status
