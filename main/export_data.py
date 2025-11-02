import os
import sys
import csv
import django
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import Crew, Customer, JobOpening

def export_model(queryset, fields, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        for obj in queryset:
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)
    print(f"✅ Exported {queryset.count()} records to {filename}")

def export_crew():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"main/crew_export_{timestamp}.csv"
    export_model(Crew.objects.all(), ['name', 'role', 'email', 'phone'], filename)

def export_customer():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"main/customer_export_{timestamp}.csv"
    export_model(Customer.objects.all(), ['name', 'email', 'phone'], filename)

def export_jobopening():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"main/jobopening_export_{timestamp}.csv"
    export_model(JobOpening.objects.all(), ['title', 'description', 'is_active'], filename)

def run_export(model_name):
    if model_name in ['crew', 'all']:
        print("📤 Exporting Crew...")
        export_crew()
    if model_name in ['customer', 'all']:
        print("📤 Exporting Customer...")
        export_customer()
    if model_name in ['jobopening', 'all']:
        print("📤 Exporting JobOpening...")
        export_jobopening()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_data.py [crew|customer|jobopening|all]")
    else:
        run_export(sys.argv[1].lower())
