import os
from flask import Flask, request, render_template, send_file
from app_2 import (
    GoalExtractor,
    EmployeeBonusProcessor,
)  # Assuming your existing logic is in app.py

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Ensure upload and output folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def upload_files():
    """
    Display the file upload form.
    """
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_files():
    try:
        # Get uploaded files
        shifts_file = request.files.get("shifts_file")
        bonus_file = request.files.get("bonus_file")

        if not shifts_file or not bonus_file:
            return "Please upload both required files.", 400

        # Save uploaded files
        shifts_file_path = os.path.join(
            app.config["UPLOAD_FOLDER"], shifts_file.filename
        )
        bonus_file_path = os.path.join(app.config["UPLOAD_FOLDER"], bonus_file.filename)

        shifts_file.save(shifts_file_path)
        bonus_file.save(bonus_file_path)

        print(f"Shifts file saved at: {shifts_file_path}")
        print(f"Bonus file saved at: {bonus_file_path}")

        # Process with GoalExtractor
        intermediate_output = os.path.join(
            app.config["OUTPUT_FOLDER"], "bonus_dates_sorted.csv"
        )
        goal_extractor = GoalExtractor(bonus_file_path, intermediate_output)
        goal_extractor.pair_and_print()

        print(f"Intermediate output generated at: {intermediate_output}")

        # Process with EmployeeBonusProcessor
        final_output = os.path.join(
            app.config["OUTPUT_FOLDER"], "final_employee_bonuses.csv"
        )
        employee_processor = EmployeeBonusProcessor(
            shifts_file_path, intermediate_output
        )
        employee_processor.process_bonuses()

        print(f"Final output generated at: {final_output}")

        # Serve the final output file
        return send_file(
            final_output, as_attachment=True, download_name="final_employee_bonuses.csv"
        )

    except Exception as e:
        print(f"Error during processing: {e}")
        return f"An error occurred during processing: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
