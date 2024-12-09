import subprocess
from goal_extractor import GoalExtractor

sorted = "bonus_app/Sorted.csv"


solu_excel = input("excel: ")


def main():
    GoalExtractor(sorted, solu_excel)
    subprocess.run(["python", "bonus_app/employee_extractor.py"])


main = main()
