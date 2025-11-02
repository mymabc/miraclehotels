import os
import sys
import csv
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import JobOpening

def parse_boolean(value):
    return value.strip().lower() in ['true', '1', 'yes']

def import_jobopening_from_csv(file_path):
    skipped = []
    imported = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            title = row.get('title', '').strip()
            description = row.get('description', '').strip()
            is_active_raw = row.get('is_active', '').strip()

            if not title or not description:
                skipped.append((i, "Missing required fields"))
                continue

            is_active = parse_boolean(is_active_raw) if is_active_raw else True

            JobOpening.objects.create(title=title, description=description, is_active=is_active)
            imported += 1

    print(f"✅ Imported {imported} job opening records.")
    if skipped:
        print("⚠️ Skipped rows:")
        for row_num, reason in skipped:
            print(f"  - Row {row_num}: {reason}")

if __name__ == "__main__":
    import_jobopening_from_csv("main/jobopening_data.csv")
