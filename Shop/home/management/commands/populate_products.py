import random
import requests
from io import BytesIO
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify
from faker import Faker
from home.models import Category, SubCategory, Product

class Command(BaseCommand):
    help = 'Populates the database with fake products using your exact category structure.'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='The number of fake products to create.')
        parser.add_argument('--clear', action='store_true', help='Deletes all products with "FAKE" in the name.')

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR('This command cannot be run in production.'))
            return

        count = options['count']
        fake = Faker()

        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing all FAKE products...'))
            # Delete products with "FAKE" in the name instead of using is_fake field
            Product.objects.filter(name__icontains='FAKE').delete()

        self.stdout.write("Ensuring your categories and subcategories exist...")
        
        # This is your exact data structure
        category_data = {
            'Digital Products': ['Laptops', 'Phones', 'Camera', 'Tablets'],
            'Kitchen': ['frying pan', 'knife', 'glass'],
            'Fashion': ['Clothing', 'Shoes', 'Accessories', 'Jewelry', 'T-Shirts', 'Jeans', 'Sneakers'],
            'Sports Gear': ['Sneakers', 'Jerseys', 'Equipment'],
        }

        # Use get_or_create to safely add this data if it doesn't exist
        all_subcategories = []
        for cat_name, sub_names in category_data.items():
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            
            for sub_name in sub_names:
                # Generate a unique slug to avoid conflicts
                unique_slug = slugify(f"{cat_name}-{sub_name}")
                
                subcategory, _ = SubCategory.objects.get_or_create(
                    category=category, 
                    name=sub_name,
                    defaults={'slug': unique_slug}
                )
                all_subcategories.append(subcategory)
        
        if not all_subcategories:
            self.stdout.write(self.style.ERROR('No subcategories found or created. Cannot create products.'))
            return
            
        self.stdout.write(f"Creating {count} fake products...")

        for i in range(count):
            self.stdout.write(f'  - Creating product {i + 1}/{count}...', ending='\r')
            
            # Pick a random existing subcategory
            random_sub_cat = random.choice(all_subcategories)
            parent_cat = random_sub_cat.category

            # Generate a shorter product name that fits in 40 characters
            base_name = fake.word().title()
            fake_name = f"FAKE {base_name} {random.randint(1, 999)}"
            
            # Ensure name doesn't exceed 40 characters
            if len(fake_name) > 40:
                fake_name = fake_name[:37] + "..."

            try:
                product = Product.objects.create(
                    category=parent_cat,
                    subcategory=random_sub_cat,
                    name=fake_name,  # Shortened name
                    description=fake.text(max_nb_chars=200),  # Limit description length too
                    price=random.randint(10, 3000),
                    availability=True,
                    count=random.randint(10, 200),
                )
                
                # Try to download and save an image
                try:
                    response = requests.get('https://picsum.photos/800/600', stream=True, timeout=5)
                    response.raise_for_status()
                    image_file = ContentFile(response.content, name=f'{product.slug}.jpg')
                    product.image.save(f'{product.slug}.jpg', image_file, save=True)
                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.WARNING(f"\nCould not download image for product {product.name}: {e}"))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\nError creating product: {e}"))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'\n\nSuccessfully created {count} fake products.'))