import os
import sys
import csv
import django
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import JobOpening

def export_jobopening_to_csv():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"main/jobopening_export_{timestamp}.csv"
    job_list = JobOpening.objects.all()

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['title', 'description', 'is_active'])  # Header
        for job in job_list:
            writer.writerow([job.title, job.description, job.is_active])

    print(f"✅ Exported {job_list.count()} job opening records to {filename}")

if __name__ == "__main__":
    export_jobopening_to_csv()
