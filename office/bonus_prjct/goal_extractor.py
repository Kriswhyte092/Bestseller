import openpyxl
import csv
from datetime import datetime


class BonusProcessorRefined:
    # Define the bonus thresholds
    bonus_thresholds = {
        80: 2000,
        100: 2000,
        115: 3000,
        130: 4000,
        150: 5000,
        175: 7500,
        200: 10000,
    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.sheet = self.load_workbook()
        self.dates = self.extract_dates()

    def load_workbook(self):
        """Load the workbook and return the active sheet."""
        workbook = openpyxl.load_workbook(self.file_path, data_only=True)
        return workbook.active

    def extract_dates(self):
        """Extract dates from the top rows of the sheet."""
        dates = []
        for cell in self.sheet[2]:
            if isinstance(cell.value, (str, datetime)):
                dates.append(cell.value)
            else:
                dates.append(None)
        return dates

    def get_bonus(self, index):
        """Get the bonus based on the index."""
        for threshold in sorted(self.bonus_thresholds.keys(), reverse=True):
            if index >= threshold:
                return self.bonus_thresholds[threshold]
        return 0

    def process_stores(self, output_file):
        """
        Process each store and write results to a CSV file.
        """
        rows = []
        for row in self.sheet.iter_rows(
            min_row=4, min_col=1, max_col=self.sheet.max_column
        ):
            store_name = row[0].value
            for i, cell in enumerate(row[1:], start=1):
                if isinstance(cell.value, str) and "%" in cell.value:
                    try:
                        index = int(cell.value.replace("%", "").strip())
                        if index >= 100 or (
                            index >= 80 and store_name in ["VMK", "VIK", "NIK"]
                        ):
                            bonus = self.get_bonus(index)
                            if self.dates[i]:
                                rows.append([self.dates[i], store_name, bonus])
                    except ValueError:
                        continue

        # Write the results to a CSV file
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Store", "Bonus"])
            writer.writerows(rows)


# File paths
refined_output_file_path = "office/bonus_prjct/refined_bonus_results.csv"

# Process the refined logic
refined_processor = BonusProcessorRefined(
    "office/bonus_prjct/Solubonusar_Bestseller_okt2024.xlsx"
)
refined_processor.process_stores(refined_output_file_path)

refined_output_file_path
