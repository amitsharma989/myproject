import csv
from django.core.management.base import BaseCommand
from app_name.models import Product

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the CSV file")
    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"] 
        products = []
        try:
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        name = row["name"]
                        category = row["category"]
                        price = float(row["price"])
                        stock = int(row["stock"])
                        if price < 0 or stock < 0:
                            self.stdout.write(f"Skipping invalid row {row}")
                            continue
                        products.append(Product(name=name, category=category, price=price, stock=stock)) 
                        if len(products) >= 500:
                            Product.objects.bulk_create(products)
                            products.clear()
                    except (ValueError, KeyError) as e:
                        self.stdout.write(f"Skipping invalid row {row} - error")    
                if products:
                    Product.objects.bulk_create(products)           
                    self.stdout.write("import completed successfully.") 
        except FileNotFoundError:
            self.stdout.write("File not found")     
        except Exception as e:
            self.stdout.write("Error occured")         