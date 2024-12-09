from datetime import datetime

class Date:
    def __init__(self, date):
        self.date = date
       
    def getDate(self):
        return self._getDate()
        
    def _getDate(self):
        dateStr = self.date
        dateObj = datetime.strptime(dateStr, "%b %d, %Y")
        day = dateObj.day
        month = dateObj.month
        year = dateObj.year
        return day, month, year

    def isWeekend(self):
        day, month, year = self._getDate()
        dt = datetime(year, month, day)
        if dt.weekday() == 5 or dt.weekday() == 6:
            return True
        return False


   
    


