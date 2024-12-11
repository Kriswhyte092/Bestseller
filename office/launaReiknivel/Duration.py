from datetime import datetime

class Duration:
    def __init__(self, start, end):
        self.start = datetime.strptime(start, "%I:%M %p")
        self.end = datetime.strptime(end, "%I:%M %p")

    def getDurationWeekEnd(self):
        EV = self.end - self.start
        DV = 0
        return DV, EV

    def getDurationWeekDay(self):
        #latePay stendur fyrir eftirvinnu for lack of a better term
        #og sma niggalicious
        dayPay, latePay = self.isOvertime()
        DV = self.formatDuration(dayPay)
        EV = 0
        if latePay != 0:
            EV = self.formatDuration(latePay)
        return DV, EV

    def formatDuration(self, td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}:{minutes}:{seconds}"
        

    def isOvertime(self):
        dayPayEnd = datetime.strptime("6:00 PM", "%I:%M %p")
        if self.end >= dayPayEnd:
            DV = dayPayEnd - self.start
            EV = self.end - dayPayEnd
            return DV, EV
        DV = self.end - self.start
        EV = 0
        return DV, EV
    


