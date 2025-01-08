from datetime import datetime

class Date:
    def __init__(self, date):
        self.date = date
       
    def getDate(self):
        day, month, year = self._getDate()
        return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"

    def isWeekend(self):
        day, month, year = self._getDate()
        dt = datetime(year, month, day)
        if dt.weekday() == 5 or dt.weekday() == 6:
            return True
        return False

    def _getDate(self):
        month, day, year = self.date.split(" ")
        day = day.replace(",", "")
        day = int(day) 
        year = int(year) 
        month = month[:3]
        month = self.mapMonth(month)
        month = int(month) 
        return day, month, year

    def mapMonth(self, month):
        months = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }
        return months[month]
