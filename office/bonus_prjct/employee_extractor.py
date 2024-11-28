import csv
import re
from collections import defaultdict


class EmployeeBonusProcessor:
    def __init__(self, shifts_file="shifts-export.csv"):
        """
        Initialize the processor with the shifts file and load the shifts data.
        """
        self.shifts_file = shifts_file
        self.shifts_data = self._load_shifts_data()

    def _load_shifts_data(self):
        """
        Load the shifts data from the CSV file into a dictionary.
        """
        shifts_data = {}
        with open(self.shifts_file, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Skip header row
            for row in reader:
                for day, shifts in zip(headers, row):
                    if day not in shifts_data:
                        shifts_data[day] = []
                    shifts_data[day].append(shifts)
        return shifts_data

    def _extract_employee(self, shift, store):
        """
        Extract the employee name from the shift information if the store matches.
        """
        if store in shift:
            match = re.search(r"\n([^\n]+)\n", shift)
            if match:
                return match.group(1).strip()
        return None

    def process_bonuses(self, bonus_file):
        """
        Process the bonuses from the bonus file and calculate the total bonuses for each employee.
        """
        employee_bonuses = defaultdict(float)
        with open(bonus_file, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                date, store, bonus = row
                bonus = float(bonus)
                if date in self.shifts_data:
                    for shift in self.shifts_data[date]:
                        employee = self._extract_employee(shift, store)
                        if employee:
                            employee_bonuses[employee] += bonus
        return employee_bonuses


# Example usage
if __name__ == "__main__":
    bonus_file = "bonuses.csv"
    processor = EmployeeBonusProcessor()
    employee_bonuses = processor.process_bonuses(bonus_file)
    for employee, total_bonus in employee_bonuses.items():
        print(f"{employee}: {total_bonus}")
