import pandas as pd
from datetime import datetime

# Load the dataset
file_path = r"laun_app\report-export.xls"
data = pd.ExcelFile(file_path)
df = data.parse("report-export")

# Clean column names
df.columns = df.columns.str.replace("\n", " ").str.strip()

# Drop rows with missing required columns
df = df.dropna(subset=["EMPLOYEE", "DATE", "CLOCK IN TIME", "CLOCK OUT TIME"])

# Define a known format for DATE parsing (adjust based on actual format in your file)
try:
    df["DATE"] = pd.to_datetime(df["DATE"], format="%b %d, %Y", errors="coerce")
except ValueError:
    print("Date parsing failed. Check the date format.")

# Ensure CLOCK IN TIME and CLOCK OUT TIME are valid
df["CLOCK IN TIME"] = pd.to_datetime(
    df["CLOCK IN TIME"], format="%I:%M %p", errors="coerce"
).dt.time
df["CLOCK OUT TIME"] = pd.to_datetime(
    df["CLOCK OUT TIME"], format="%I:%M %p", errors="coerce"
).dt.time

# Drop rows where DATE or TIME columns couldn't be parsed
df = df.dropna(subset=["DATE", "CLOCK IN TIME", "CLOCK OUT TIME"])


# Function to calculate regular and overtime hours
def calculate_hours(row):
    date = row["DATE"]
    clock_in = datetime.combine(date, row["CLOCK IN TIME"])
    clock_out = datetime.combine(date, row["CLOCK OUT TIME"])

    regular_hours = 0
    overtime_hours = 0

    # Check if the day is a weekend
    is_weekend = date.weekday() >= 5  # Saturday (5) or Sunday (6)

    # Define cutoff for regular hours (6 PM)
    regular_cutoff = datetime.combine(
        date, datetime.strptime("6:00 PM", "%I:%M %p").time()
    )

    # Calculate hours
    if is_weekend:
        overtime_hours = (clock_out - clock_in).total_seconds() / 3600
    else:
        if clock_out <= regular_cutoff:
            regular_hours = (clock_out - clock_in).total_seconds() / 3600
        elif clock_in >= regular_cutoff:
            overtime_hours = (clock_out - clock_in).total_seconds() / 3600
        else:
            regular_hours = (regular_cutoff - clock_in).total_seconds() / 3600
            overtime_hours = (clock_out - regular_cutoff).total_seconds() / 3600

    return pd.Series([regular_hours, overtime_hours])


# Apply the function to calculate hours
df[["REGULAR HOURS", "OVERTIME HOURS"]] = df.apply(calculate_hours, axis=1)

# Summarize by employee
summary = (
    df.groupby("EMPLOYEE")[["REGULAR HOURS", "OVERTIME HOURS"]].sum().reset_index()
)

# Save results to CSV
output_path = r"laun_app\employee_hours_summary.csv"
summary.to_csv(output_path, index=False)

print(f"Summary saved to: {output_path}")
