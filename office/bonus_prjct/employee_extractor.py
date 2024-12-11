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

    def _preprocess_bonuses(self, bonus_file):
        """
        Preprocess the bonus file to ensure correct headers and formatting.
        """
        bonuses = pd.read_csv(bonus_file, encoding="latin1", header=None)

        # Check and rename columns dynamically if required
        if bonuses.shape[1] == 3:
            bonuses.columns = ["Date", "Store", "Bonus"]
        else:
            raise ValueError("Unexpected file structure in bonuses file.")

        # Clean and normalize data
        bonuses["Date"] = bonuses["Date"].str.strip()
        bonuses["Store"] = bonuses["Store"].str.strip()
        bonuses["Bonus"] = bonuses["Bonus"].astype(float)

        return bonuses

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
        bonuses = self._preprocess_bonuses(self.bonus_file)
        employee_bonuses = defaultdict(float)

        for _, row in bonuses.iterrows():
            date, store, bonus = row["Date"], row["Store"], row["Bonus"]
            if date in self.shifts_data:
                for shift in self.shifts_data[date]:
                    employees = self._extract_employees(shift, store)
                    for employee in employees:
                        employee_bonuses[employee] += bonus

        return employee_bonuses


# Load the provided data files
shifts_file_path = "office/bonus_prjct/shifts.csv"
bonus_file_path = "office/bonus_prjct/output.csv"  # Change to the desired file

# Run the processor
processor = EmployeeBonusProcessor(shifts_file_path, bonus_file_path)
employee_bonuses = processor.process_bonuses()

for employee, bonus in employee_bonuses.items():
    print(f"{employee}: {bonus}")

import csv


def save_bonuses_to_csv(employee_bonuses, output_file):
    """
    Save the employee bonuses to a CSV file.
    """
    with open(output_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Employee", "Bonus"])
        for employee, bonus in employee_bonuses.items():
            writer.writerow([employee, bonus])


output_file_path = "employee_bonuses.csv"
save_bonuses_to_csv(employee_bonuses, output_file_path)
