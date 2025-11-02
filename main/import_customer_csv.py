import os
import sys
import csv
import re
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import Customer

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def import_customer_from_csv(file_path):
    skipped = []
    imported = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            name = row.get('name', '').strip()
            email = row.get('email', '').strip()
            phone = row.get('phone', '').strip()

            if not name or not email or not phone:
                skipped.append((i, "Missing required fields"))
                continue

            if not is_valid_email(email):
                skipped.append((i, "Invalid email format"))
                continue

            if Customer.objects.filter(email=email).exists():
                skipped.append((i, "Duplicate email"))
                continue

            Customer.objects.create(name=name, email=email, phone=phone)
            imported += 1

    print(f"✅ Imported {imported} customer records.")
    if skipped:
        print("⚠️ Skipped rows:")
        for row_num, reason in skipped:
            print(f"  - Row {row_num}: {reason}")

if __name__ == "__main__":
    import_customer_from_csv("main/customer_data.csv")
