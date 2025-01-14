from utils.launaReiknivel.createShift import *
from data.launaReiknivel.dataBase import *
from data.utils.checkDb import checkDb
import psycopg2
from psycopg2 import sql

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
        self.checkDb = checkDb()

    def exportEmployee(self):


    def shiftToExport(self):
        print(self.checkDb)
        DV, EV = self.shift.getDuration()
        return self.shift.getEmployee(), self.shift.getDate(), DV, EV

    def exportToDb(self):
        location = self.shift.getLocation()
        employee, date, DV, EV = self.shiftToExport()
        print(employee, date, DV, EV)
        db_name = self.checkDb
        try:
            db = dataBase(db_name)
            if db.tableExists(employee):
                query = sql.SQL("INSERT INTO {} (date, dv, ev, location) VALUES (%s, %s, %s, %s)").format(
                    sql.Identifier(employee)
                )
                db.executeQuery(query, (date, DV, EV, location)) 
                db.commit()
                print(f"shift for {employee} exported to db")
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()  
        finally:
            db.close()



