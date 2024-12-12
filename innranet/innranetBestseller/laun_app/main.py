from laun_app_code import DataExtraction

input_file = r"report-export.xls"
output_file = "summary.csv"

processor = DataExtraction(input_file, output_file)
processor.process_data()

print(f"Output file created: {output_file}")
