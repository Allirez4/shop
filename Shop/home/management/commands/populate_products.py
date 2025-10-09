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
        parser.add_argument('--bulk', action='store_true', help='Use bulk create (faster, no images).')
        parser.add_argument('--threads', type=int, default=10, help='Number of threads for image downloads.')

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR('This command cannot be run in production.'))
            return

        count = options['count']
        use_bulk = options['bulk']
        fake = Faker()

        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing all FAKE products...'))
            Product.objects.filter(name__icontains='FAKE').delete()

        self.stdout.write("Ensuring your categories and subcategories exist...")
        
        category_data = {
            'Digital Products': ['Laptops', 'Phones', 'Camera', 'Tablets'],
            'Kitchen': ['frying pan', 'knife', 'glass'],
            'Fashion': ['Clothing', 'Shoes', 'Accessories', 'Jewelry', 'T-Shirts', 'Jeans', 'Sneakers'],
            'Sports Gear': ['Sneakers', 'Jerseys', 'Equipment'],
        }

        all_subcategories = []
        for cat_name, sub_names in category_data.items():
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            
            for sub_name in sub_names:
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

        if use_bulk:
            # BULK CREATE - VERY FAST (No images)
            self.stdout.write(f"Creating {count} fake products using bulk create...")
            products_to_create = []
            
            for i in range(count):
                random_sub_cat = random.choice(all_subcategories)
                parent_cat = random_sub_cat.category
                base_name = fake.word().title()
                fake_name = f"FAKE {base_name} {random.randint(1, 999)}"
                
                if len(fake_name) > 40:
                    fake_name = fake_name[:37] + "..."
                
                # Generate unique slug
                base_slug = slugify(fake_name)
                slug = f"{base_slug}-{i}"
                
                products_to_create.append(Product(
                    category=parent_cat,
                    subcategory=random_sub_cat,
                    name=fake_name,
                    slug=slug,
                    description=fake.text(max_nb_chars=200),
                    price=random.randint(10, 3000),
                    availability=True,
                    count=random.randint(10, 200),
                ))
                
                if (i + 1) % 50 == 0:
                    self.stdout.write(f'  - Prepared {i + 1}/{count} products...', ending='\r')
            
            # Bulk insert all at once
            Product.objects.bulk_create(products_to_create, batch_size=100)
            self.stdout.write(self.style.SUCCESS(f'\n\nSuccessfully created {count} fake products (bulk mode).'))
            
        else:
            # REGULAR CREATE WITH MULTITHREADING FOR IMAGES
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            self.stdout.write(f"Creating {count} fake products with images (using {options['threads']} threads)...")
            
            def create_product_with_image(i):
                random_sub_cat = random.choice(all_subcategories)
                parent_cat = random_sub_cat.category
                base_name = fake.word().title()
                fake_name = f"FAKE {base_name} {random.randint(1, 999)}"
                
                if len(fake_name) > 40:
                    fake_name = fake_name[:37] + "..."

                try:
                    product = Product.objects.create(
                        category=parent_cat,
                        subcategory=random_sub_cat,
                        name=fake_name,
                        description=fake.text(max_nb_chars=200),
                        price=random.randint(10, 3000),
                        availability=True,
                        count=random.randint(10, 200),
                    )
                    
                    # Download image with shorter timeout
                    try:
                        response = requests.get('https://picsum.photos/800/600', stream=True, timeout=3)
                        response.raise_for_status()
                        image_file = ContentFile(response.content, name=f'{product.slug}.jpg')
                        product.image.save(f'{product.slug}.jpg', image_file, save=True)
                        return (True, None)
                    except requests.exceptions.RequestException as e:
                        return (True, f"No image for {product.name}")
                        
                except Exception as e:
                    return (False, str(e))
            
            # Use ThreadPoolExecutor for parallel image downloads
            with ThreadPoolExecutor(max_workers=options['threads']) as executor:
                futures = [executor.submit(create_product_with_image, i) for i in range(count)]
                
                completed = 0
                for future in as_completed(futures):
                    completed += 1
                    success, error = future.result()
                    if error:
                        self.stdout.write(f'\r  - Progress: {completed}/{count} (Warning: {error})', ending='')
                    else:
                        self.stdout.write(f'\r  - Progress: {completed}/{count}', ending='')
            
            self.stdout.write(self.style.SUCCESS(f'\n\nSuccessfully created {count} fake products.'))



"""



python manage.py populate_products --count=250 --threads=20
python manage.py populate_products --count=250 --bulk --clear #with no image and clearing the data base#

python manage.py populate_products --count=250 --threads=15

"""