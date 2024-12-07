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
        # File paths
        intermediate_output = os.path.join(
            app.config["OUTPUT_FOLDER"], "bonus_dates_sorted.csv"
        )
        final_output = os.path.join(
            app.config["OUTPUT_FOLDER"], "final_employee_bonuses.csv"
        )

        # Confirm file operations
        print(f"Intermediate file exists: {os.path.exists(intermediate_output)}")
        if os.path.exists(intermediate_output):
            with open(intermediate_output, "r") as f:
                print(f"Intermediate file content:\n{f.read()}")

        print(f"Final file exists: {os.path.exists(final_output)}")
        if os.path.exists(final_output):
            with open(final_output, "r") as f:
                print(f"Final file content:\n{f.read()}")

        return send_file(
            final_output, as_attachment=True, download_name="final_employee_bonuses.csv"
        )

    except Exception as e:
        print(f"Error during processing: {e}")
        return f"An error occurred during processing: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
