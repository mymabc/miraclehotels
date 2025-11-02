import os
import sys
import csv
import django
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miraclehotels.settings")
django.setup()

from main.models import Customer

def export_customer_to_csv():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"main/customer_export_{timestamp}.csv"
    customer_list = Customer.objects.all()

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'email', 'phone'])  # Header
        for customer in customer_list:
            writer.writerow([customer.name, customer.email, customer.phone])

    print(f"✅ Exported {customer_list.count()} customer records to {filename}")

if __name__ == "__main__":
    export_customer_to_csv()
