import os
import sys
import csv
import django
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import Crew

def export_crew_to_csv():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"main/crew_export_{timestamp}.csv"
    crew_list = Crew.objects.all()

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'role', 'email', 'phone'])  # Header
        for crew in crew_list:
            writer.writerow([crew.name, crew.role, crew.email, crew.phone])

    print(f"✅ Exported {crew_list.count()} crew records to {filename}")

if __name__ == "__main__":
    export_crew_to_csv()
