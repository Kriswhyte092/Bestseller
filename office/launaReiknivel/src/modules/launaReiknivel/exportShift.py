from utils.launaReiknivel.createShift import *
from data.launaReiknivel.dataBase import *

class exportShift:
    def __init__(self, name, id, date, location, clockIn, clockOut, status):
        self.shift = createShift(
            name=name,
            id=id,
            date=date,
            location=location,
            clockIn=clockIn,
            clockOut=clockOut,
            status=status
        )

    def shiftToExport(self):
        DV, EV = self.shift.getDuration()
        return self.shift.getEmployee(), self.shift.getDate(), DV, EV

    def exportToDb(self):
        employee, date, DV, EV = self.shiftToExport()
        print(employee, date, DV, EV)
        try:
            db = dataBase("launaReiknivel.db")
            if db.tableExists(employee):
                query = f"INSERT INTO {employee} (date, dv, ev) VALUES (?, ?, ?)"
                db.executeQuery(query, (date, DV, EV)) 
                db.commit()
                print(f"shift for {employee} exported to db")
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()  
        finally:
            db.close()
