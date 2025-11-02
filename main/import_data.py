import os
import sys
import csv
import re
import logging
import argparse
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import Crew, Customer, JobOpening

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "import_log.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def parse_boolean(value):
    return value.strip().lower() in ['true', '1', 'yes']

def import_crew(file_path):
    skipped, imported = [], 0
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            name = row.get('name', '').strip()
            role = row.get('role', '').strip()
            email = row.get('email', '').strip()
            phone = row.get('phone', '').strip()

            if not name or not role or not email or not phone:
                reason = "Missing required fields"
                skipped.append((i, reason))
                logging.warning(f"Crew row {i} skipped: {reason}")
                continue
            if not is_valid_email(email):
                reason = "Invalid email format"
                skipped.append((i, reason))
                logging.warning(f"Crew row {i} skipped: {reason}")
                continue
            if Crew.objects.filter(email=email).exists():
                reason = "Duplicate email"
                skipped.append((i, reason))
                logging.warning(f"Crew row {i} skipped: {reason}")
                continue

            Crew.objects.create(name=name, role=role, email=email, phone=phone)
            imported += 1
            logging.info(f"Crew row {i} imported: {name}, {role}")
    return imported, skipped

def import_customer(file_path):
    skipped, imported = [], 0
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            name = row.get('name', '').strip()
            email = row.get('email', '').strip()
            phone = row.get('phone', '').strip()

            if not name or not email or not phone:
                reason = "Missing required fields"
                skipped.append((i, reason))
                logging.warning(f"Customer row {i} skipped: {reason}")
                continue
            if not is_valid_email(email):
                reason = "Invalid email format"
                skipped.append((i, reason))
                logging.warning(f"Customer row {i} skipped: {reason}")
                continue
            if Customer.objects.filter(email=email).exists():
                reason = "Duplicate email"
                skipped.append((i, reason))
                logging.warning(f"Customer row {i} skipped: {reason}")
                continue

            Customer.objects.create(name=name, email=email, phone=phone)
            imported += 1
            logging.info(f"Customer row {i} imported: {name}")
    return imported, skipped

def import_jobopening(file_path):
    skipped, imported = [], 0
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            title = row.get('title', '').strip()
            description = row.get('description', '').strip()
            is_active_raw = row.get('is_active', '').strip()

            if not title or not description:
                reason = "Missing required fields"
                skipped.append((i, reason))
                logging.warning(f"JobOpening row {i} skipped: {reason}")
                continue

            is_active = parse_boolean(is_active_raw) if is_active_raw else True
            JobOpening.objects.create(title=title, description=description, is_active=is_active)
            imported += 1
            logging.info(f"JobOpening row {i} imported: {title}")
    return imported, skipped

def run_import(model_name, reset=False):
    base_path = os.path.join('main')
    summary = {}

    if model_name in ['crew', 'all']:
        if reset:
            Crew.objects.all().delete()
            logging.info("🔄 Reset: All Crew records deleted.")
            print("🧹 Crew table cleared.")
        print("📥 Importing Crew...")
        imported, skipped = import_crew(os.path.join(base_path, 'crew_data.csv'))
        summary['Crew'] = (imported, skipped)

    if model_name in ['customer', 'all']:
        if reset:
            Customer.objects.all().delete()
            logging.info("🔄 Reset: All Customer records deleted.")
            print("🧹 Customer table cleared.")
        print("📥 Importing Customer...")
        imported, skipped = import_customer(os.path.join(base_path, 'customer_data.csv'))
        summary['Customer'] = (imported, skipped)

    if model_name in ['jobopening', 'all']:
        if reset:
            JobOpening.objects.all().delete()
            logging.info("🔄 Reset: All JobOpening records deleted.")
            print("🧹 JobOpening table cleared.")
        print("📥 Importing JobOpening...")
        imported, skipped = import_jobopening(os.path.join(base_path, 'jobopening_data.csv'))
        summary['JobOpening'] = (imported, skipped)

    for model, (count, skipped) in summary.items():
        print(f"✅ Imported {count} {model} records.")
        logging.info(f"✅ Imported {count} {model} records.")
        if skipped:
            print(f"⚠️ Skipped {len(skipped)} {model} rows:")
            for row_num, reason in skipped:
                print(f"  - Row {row_num}: {reason}")
            logging.info(f"⚠️ Skipped {len(skipped)} {model} rows.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import data into Django models.")
    parser.add_argument("model", choices=["crew", "customer", "jobopening", "all"], help="Model to import")
    parser.add_argument("--reset", action="store_true", help="Delete existing records before import")
    args = parser.parse_args()

    run_import(args.model.lower(), reset=args.reset)
