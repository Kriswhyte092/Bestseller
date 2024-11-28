import pandas as pd
from collections import defaultdict
import re


class EmployeeBonusProcessor:
    def __init__(self, shifts_file, bonus_file):
        """
        Initialize the processor with the shifts and bonuses file paths.
        """
        self.shifts_file = shifts_file
        self.bonus_file = bonus_file
        self.shifts_data = self._load_shifts_data()

    def _load_shifts_data(self):
        """
        Load the shifts data into a dictionary keyed by date.
        """
        shifts = pd.read_csv(self.shifts_file, encoding="utf-8")
        shifts_data = defaultdict(list)
        for day in shifts.columns:
            for row in shifts[day].dropna():
                date_match = re.match(r"(\d+\s\w+)", row)
                if date_match:
                    date = date_match.group(1)
                    shifts_data[date].append(row)
        return shifts_data

    def _extract_employees(self, shift, store):
        """
        Extract employees working at a specific store in a shift entry.
        """
        employees = []
        lines = shift.split("\n")
        for i, line in enumerate(lines):
            if store in line:
                # The employee name is typically the following line after the store information
                if i + 1 < len(lines):
                    employee_name = lines[i + 1].strip()
                    if employee_name:
                        employees.append(employee_name)
        return employees

    def process_bonuses(self):
        """
        Process the bonuses from the bonuses file and assign them to employees.
        """
        bonuses = pd.read_csv(
            self.bonus_file, header=None, names=["Date", "Store", "Bonus"]
        )
        employee_bonuses = defaultdict(float)

        for _, row in bonuses.iterrows():
            date, store, bonus = row["Date"], row["Store"], float(row["Bonus"])
            if date in self.shifts_data:
                for shift in self.shifts_data[date]:
                    employees = self._extract_employees(shift, store)
                    for employee in employees:
                        employee_bonuses[employee] += bonus

        return employee_bonuses


# Load the provided data files
shifts_file_path = "office/bonus_prjct/shifts-export.csv"
bonus_file_path = "office/bonus_prjct/bullshit.csv"

# Run the processor
processor = EmployeeBonusProcessor(shifts_file_path, bonus_file_path)
employee_bonuses = processor.process_bonuses()

for employee, bonus in employee_bonuses.items():
    print(f"{employee}: {bonus}")
