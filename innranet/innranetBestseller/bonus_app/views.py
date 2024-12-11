import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from bonus_app.bonus_app_code import GoalExtractor, EmployeeBonusProcessor


def upload_files(request):
    # Ensure directories exist
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    os.makedirs(settings.OUTPUTS_ROOT, exist_ok=True)

    if request.method == "POST":
        # Get the uploaded files
        shifts_file = request.FILES.get("shifts_file")
        bonus_file = request.FILES.get("bonus_file")

        if not shifts_file or not bonus_file:
            return HttpResponse("Please upload both required files.", status=400)

        # Save files to disk
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        shifts_file_path = fs.save(shifts_file.name, shifts_file)
        bonus_file_path = fs.save(bonus_file.name, bonus_file)

        # Process files
        output_csv_path = os.path.join(settings.OUTPUTS_ROOT, "bonus_dates_sorted.csv")
        goal_extractor = GoalExtractor(bonus_file_path, output_csv_path)
        goal_extractor.pair_and_print()

        final_output_path = os.path.join(
            settings.OUTPUTS_ROOT, "final_employee_bonuses.csv"
        )
        employee_processor = EmployeeBonusProcessor(shifts_file_path, output_csv_path)
        employee_processor.process_bonuses()

        # Serve the final CSV file as a response
        with open(final_output_path, "rb") as f:
            response = HttpResponse(f, content_type="application/csv")
            response["Content-Disposition"] = (
                "attachment; filename=final_employee_bonuses.csv"
            )
            return response

    # Render the form for GET requests
    return render(request, "bonus_app/index.html")


def process_files(request):
    if request.method == "POST":
        # Ensure directories exist
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        # Get the uploaded files
        shifts_file = request.FILES.get("shifts_file")
        bonus_file = request.FILES.get("bonus_file")

        if not shifts_file or not bonus_file:
            return JsonResponse({"error": "Please upload both files."}, status=400)

        # Save files to disk
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        shifts_file_path = os.path.join(
            settings.MEDIA_ROOT, fs.save(shifts_file.name, shifts_file)
        )
        bonus_file_path = os.path.join(
            settings.MEDIA_ROOT, fs.save(bonus_file.name, bonus_file)
        )

        print(f"Shifts file path: {shifts_file_path}")
        print(f"Bonus file path: {bonus_file_path}")

        # Process files
        output_csv_path = os.path.join(settings.MEDIA_ROOT, "bonus_dates_sorted.csv")
        goal_extractor = GoalExtractor(bonus_file_path, output_csv_path)
        goal_extractor.pair_and_print()

        # Assume the final file is written in the project root
        final_output_path = os.path.join(
            settings.BASE_DIR, "final_employee_bonuses.csv"
        )

        print(f"Final output path: {final_output_path}")

        # Return the processed file as a download
        if os.path.exists(final_output_path):
            with open(final_output_path, "rb") as f:
                response = HttpResponse(f, content_type="application/csv")
                response["Content-Disposition"] = (
                    "attachment; filename=final_employee_bonuses.csv"
                )
                return response
        else:
            return JsonResponse(
                {"error": "Failed to generate the output file."}, status=500
            )

    return JsonResponse({"error": "Invalid request method."}, status=405)
