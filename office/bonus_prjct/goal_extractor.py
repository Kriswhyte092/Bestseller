import openpyxl


class BonusProcessor:
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
        workbook = openpyxl.load_workbook(self.file_path)
        return workbook.active

    def extract_dates(self):
        """Extract dates from the first row of the sheet."""
        return [cell.value for cell in self.sheet[1]]

    def get_bonus(self, index):
        """Get the bonus based on the index."""
        for threshold in sorted(self.bonus_thresholds.keys(), reverse=True):
            if index >= threshold:
                return self.bonus_thresholds[threshold]
        return 0

    def process_stores(self):
        """Process each store and print the store name, date, index, and bonus."""
        for row in self.sheet.iter_rows(
            min_row=4, max_row=14, min_col=1, max_col=self.sheet.max_column
        ):
            store_name = row[0].value
            for i, cell in enumerate(row[1:], start=1):
                index_str = cell.value
                if isinstance(index_str, str) and index_str.endswith("%"):
                    try:
                        index = int(index_str[:-1])
                        if index >= 100 or (
                            index > 0 and store_name in ["VMK", "VIK", "NIK"]
                        ):
                            bonus = self.get_bonus(index)
                            print(
                                f"Store: {store_name}, Date: {self.dates[i]}, Index: {index}, Bonus: {bonus}"
                            )
                    except ValueError:
                        print(
                            f"Invalid index value: {index_str} for store {store_name} on date {self.dates[i]}"
                        )


def main():
    """Main function to execute the script."""
    file_path = r"office/bonus_prjct/Solubonusar_Bestseller_okt2024.xlsx"
    processor = BonusProcessor(file_path)
    processor.process_stores()


if __name__ == "__main__":
    main()
