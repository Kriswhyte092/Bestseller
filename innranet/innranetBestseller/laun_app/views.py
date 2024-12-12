import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from laun_app.laun_app_code import DataExtraction

def process_data_file(request):
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    os.makedirs(settings.OUTPUTS_ROOT, exist_ok=True)

    if request.method == "POST":
        # Validate uploaded file
        input_file = request.FILES.get("input_file")
        if not input_file:
            return HttpResponse("Please upload a file.", status=400)

        # Save input file
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        input_file_path = fs.save(input_file.name, input_file)
        input_file_path = os.path.join(settings.MEDIA_ROOT, input_file_path)

        # Define output path
        final_output_path = os.path.join(
            settings.OUTPUTS_ROOT, "summary.csv"
        )

        # Process the file
        try:
            processor = DataExtraction(input_file_path, final_output_path)
            processor.process_data()
        except Exception as e:
            return HttpResponse(f"Error processing file: {str(e)}", status=500)

        # Serve the final CSV file as a response
        with open(final_output_path, "rb") as f:
            response = HttpResponse(f, content_type="application/csv")
            response["Content-Disposition"] = (
                "attachment; filename=summary.csv"
            )
            return response

    # Render upload page for GET requests
    return render(request, "laun_app/upload.html")
