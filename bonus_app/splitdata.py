import csv

# Input and output file paths
input_file = "input.csv"  # Replace with your file name
output_file = "output.csv"

# Read the input file and process the data
with open(input_file, mode='r', encoding='utf-8') as infile:
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        writer.writerow(["Employee", "Bonus"])

        # Process each row
        for row in reader:
            if row and ',' in row[0]:  # Ensure the row is non-empty and has a comma
                try:
                    employee, bonus = row[0].split(',', 1)  # Split into two parts
                    writer.writerow([employee.strip(), bonus.strip()])
                except ValueError as e:
                    print(f"Skipping malformed row: {row} - Error: {e}")

print(f"Data has been successfully split into columns and saved in {output_file}.")

