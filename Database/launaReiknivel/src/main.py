#from data.launaReiknivel.loadData import *
from api.personas_api import fetch_personas
from api.shift_api import fetch_shifts
from processing.data_cleaner import validate_personas, validate_shifts
from processing.payroll_calculator import *
import pathlib
import openpyxl
import datetime

from config import config

def main():
    #sækja data frá API
    personas = fetch_personas(config.API_URL, config.API_KEY)
    #print(personas)
    shifts = fetch_shifts(config.API_URL, config.API_KEY)
    #print(shifts)

    # #validatea dataið
    validated_users, validated_locations, validated_positions = validate_personas(personas)
    validated_shifts = validate_shifts(shifts)
    
    #setja data i db
    # db = Database()
    # db.store_personas(validated_personas)
    # db.store_shifts(validated_shifts)

    #reikna payroll
    payroll_data = payroll_calculator().calculate_payroll(validated_users, validated_shifts)
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Paryoll Data"

    headers = list(payroll_data[0].keys())
    ws.append(headers)

    for val in payroll_data:
        ws.append(list(val.values()))

    workingDir = pathlib.Path(__file__).parent.resolve()
    output_file = f"{str(workingDir)}/payroll_data_{datetime.datetime.now().strftime("%B")}.xlsx"
    wb.save(output_file)
    # db.store_payroll(payroll_data)
   # generate_payslipts(payroll_data)
   # generate_summary_report(paryoll_data)


if __name__ == "__main__":
    #schedule_task(main, f"{config.SCHEDULED_TASK_DAY} {config.SCHEDULED_TASK_TIME} monthly")
    main()







"""
def main():
    workingDir = pathlib.Path(__file__).parent.resolve()
    fileName = f"{str(workingDir)}/data/launaReiknivel/launaReiknivel.xlsx"
    loadData(fileName).openExcelFile()
    


if __name__ == "__main__":
    main()
"""
