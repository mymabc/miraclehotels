import os
import sys
import csv
import re
import django

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import Crew

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def import_crew_from_csv(file_path):
    skipped = []
    imported = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            name = row.get('name', '').strip()
            role = row.get('role', '').strip()
            email = row.get('email', '').strip()
            phone = row.get('phone', '').strip()

            # Basic validation
            if not name or not role or not email or not phone:
                skipped.append((i, "Missing required fields"))
                continue

            if not is_valid_email(email):
                skipped.append((i, "Invalid email format"))
                continue

            if Crew.objects.filter(email=email).exists():
                skipped.append((i, "Duplicate email"))
                continue

            # Create record
            Crew.objects.create(name=name, role=role, email=email, phone=phone)
            imported += 1

    print(f"✅ Imported {imported} crew records.")
    if skipped:
        print("⚠️ Skipped rows:")
        for row_num, reason in skipped:
            print(f"  - Row {row_num}: {reason}")

if __name__ == "__main__":
    import_crew_from_csv("main/crew_data.csv")  # Adjust path if needed



'''
import os
import sys
import csv
import django

# Add your project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import Crew

def import_crew_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Crew.objects.create(
                name=row['name'],
                role=row['role'],
                email=row['email'],
                phone=row['phone']
            )
    print("✅ CSV import completed.")

if __name__ == "__main__":
    import_crew_from_csv("main/crew_data.csv")  # Replace with your actual path if needed

'''