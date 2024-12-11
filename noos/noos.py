import csv

def print_csv_values_in_line(filename):
    """
    Reads a CSV file and prints the values from the first column
    in a single line, separated by '..'.
    
    :param filename: The path to the CSV file.
    """
    try:
        values = []
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Ensure the row is not empty
                    values.append(str(row[0]))
        # Join the values with '..' and print
        output = '|'.join(values) + '|'
        print(output)
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_csv_file.csv' with the path to your CSV file
print_csv_values_in_line('book.csv')


