import openpyxl

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


# Function to get the bonus based on the index
def get_bonus(index):
    for threshold in sorted(bonus_thresholds.keys(), reverse=True):
        if index >= threshold:
            return bonus_thresholds[threshold]
    return 0


# Load the workbook and select the active sheet
workbook = openpyxl.load_workbook(
    r"office/bonus_prjct/Solubonusar_Bestseller_okt2024.xlsx"
)
sheet = workbook.active

# Extract dates from the first row
dates = [cell.value for cell in sheet[1]]

# Process each store (assuming stores are in rows 4-14)
for row in sheet.iter_rows(min_row=4, max_row=14, min_col=1, max_col=sheet.max_column):
    store_name = row[0].value
    for i, cell in enumerate(row[1:], start=1):
        index_str = cell.value
        if isinstance(index_str, str) and index_str.endswith("%"):
            index = int(index_str[:-1])
            if index >= 100 or (index > 0 and store_name in ["VMK", "VIK", "NIK"]):
                bonus = get_bonus(index)
                print(f"Store: {store_name}, Date: {dates[i]}, Bonus: {bonus}")
