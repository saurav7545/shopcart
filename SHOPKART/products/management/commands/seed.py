from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = "Seed database with 100 sample products"

    CATEGORIES = [
        ("Mobile", "mobile"),
        ("Fashion", "fashion"),
        ("Laptop", "laptop"),
        ("Home", "home"),
        ("Grocery", "grocery"),
        ("Beauty", "beauty"),
    ]

    PRODUCTS_BY_CATEGORY = {
        "Mobile": [
            ("iPhone 15 Pro", "Apple", 99999, 10, 4.5),
            ("Samsung Galaxy S24", "Samsung", 89999, 15, 4.3),
            ("OnePlus 12", "OnePlus", 64999, 20, 4.4),
            ("Xiaomi 14 Pro", "Xiaomi", 59999, 25, 4.2),
            ("Vivo V29", "Vivo", 39999, 30, 4.0),
            ("Realme GT 5", "Realme", 44999, 20, 4.1),
            ("Motorola Edge 50", "Motorola", 34999, 35, 3.9),
            ("iQOO 12", "iQOO", 49999, 18, 4.2),
            ("Nothing Phone 2", "Nothing", 54999, 12, 4.3),
            ("Poco F6 Pro", "Poco", 34999, 22, 4.0),
            ("Oppo Find X7", "Oppo", 54999, 15, 4.2),
            ("Honor 200", "Honor", 42999, 20, 4.1),
            ("Asus ROG Phone 8", "Asus", 79999, 8, 4.4),
            ("Google Pixel 8", "Google", 69999, 10, 4.5),
            ("Sony Xperia 1 V", "Sony", 84999, 7, 4.2),
            ("Lenovo Legion Phone", "Lenovo", 59999, 9, 4.1),
            ("Infinix Zero 30", "Infinix", 24999, 40, 3.8),
        ],
        "Fashion": [
            ("Nike Air Max", "Nike", 8999, 50, 4.2),
            ("Adidas Ultraboost", "Adidas", 9499, 45, 4.3),
            ("Puma RS-X", "Puma", 6499, 60, 4.0),
            ("New Balance 574", "New Balance", 7999, 35, 4.1),
            ("Reebok Classic", "Reebok", 5499, 55, 3.9),
            ("Levi's 501 Jeans", "Levi's", 3999, 80, 4.2),
            ("Levi's Sherpa Jacket", "Levi's", 5999, 30, 4.0),
            ("Zara Cotton Shirt", "Zara", 2999, 70, 3.8),
            ("H&M Slim Fit Pants", "H&M", 1999, 100, 3.7),
            ("Uniqlo U T-Shirt", "Uniqlo", 999, 120, 4.0),
            ("Ray-Ban Aviator", "Ray-Ban", 3499, 40, 4.3),
            ("Oakley Sunglasses", "Oakley", 4999, 25, 4.4),
            ("Adidas Track Pants", "Adidas", 2499, 80, 3.9),
            ("Nike Dri-FIT Tee", "Nike", 1499, 150, 4.0),
            ("Puma Sneakers", "Puma", 4499, 45, 4.1),
            ("Skechers Walk", "Skechers", 3999, 60, 3.9),
            ("Casio Watch", "Casio", 2499, 70, 4.1),
        ],
        "Laptop": [
            ("MacBook Pro 16", "Apple", 199999, 15, 4.7),
            ("MacBook Air 15", "Apple", 129999, 20, 4.6),
            ("Dell XPS 15", "Dell", 129999, 25, 4.3),
            ("Dell Inspiron 16", "Dell", 69999, 40, 4.0),
            ("HP Spectre x360", "HP", 119999, 18, 4.4),
            ("HP Pavilion 15", "HP", 54999, 45, 3.9),
            ("Lenovo ThinkPad X1", "Lenovo", 149999, 12, 4.5),
            ("Lenovo IdeaPad 5", "Lenovo", 49999, 50, 4.0),
            ("Asus ZenBook 14", "Asus", 79999, 30, 4.2),
            ("Asus VivoBook 16", "Asus", 44999, 55, 3.8),
            ("Acer Swift 3", "Acer", 59999, 35, 4.0),
            ("Acer Aspire 5", "Acer", 39999, 60, 3.8),
            ("MSI Modern 14", "MSI", 74999, 22, 4.1),
            ("MSI GF63 Thin", "MSI", 89999, 15, 4.2),
            ("Huawei MateBook", "Huawei", 84999, 18, 4.1),
            ("Microsoft Surface", "Microsoft", 159999, 10, 4.5),
            ("Google Pixelbook", "Google", 139999, 8, 4.3),
        ],
        "Home": [
            ("LED TV 55", "Samsung", 49999, 12, 4.4),
            ("LED TV 65", "Samsung", 69999, 8, 4.5),
            ("Air Conditioner", "Voltas", 24999, 20, 3.9),
            ("Washing Machine", "Samsung", 34999, 15, 4.1),
            ("Refrigerator", "LG", 39999, 12, 4.2),
            ("Microwave Oven", "Panasonic", 14999, 25, 4.0),
            ("Coffee Maker", "Bosch", 19999, 18, 4.3),
            ("Blender", "Philips", 7999, 35, 4.0),
            ("Vacuum Cleaner", "Dyson", 29999, 10, 4.4),
            ("Iron Box", "Philips", 3999, 40, 3.8),
            ("Table Lamp", "IKEA", 2499, 50, 4.0),
            ("Bedside Lamp", "IKEA", 1499, 60, 3.9),
            ("Wall Clock", "Casio", 1299, 70, 4.1),
            ("Bedsheet Set", "Sleepwell", 4999, 30, 4.0),
            ("Cushion Set", "IKEA", 2999, 45, 3.7),
            ("Storage Box", "IRIS", 799, 80, 3.8),
            ("Door Mat", "IRIS", 599, 65, 3.6),
        ],
        "Grocery": [
            ("Basmati Rice 10kg", "India", 899, 200, 4.0),
            ("Basmati Rice 5kg", "India", 499, 300, 4.0),
            ("Wheat Flour 10kg", "Aashirvaad", 599, 150, 4.1),
            ("Toor Dal 5kg", "Toor", 399, 200, 4.0),
            ("Sugar 5kg", "India", 399, 250, 3.9),
            ("Tea Premium", "Wagh Bakri", 499, 180, 4.2),
            ("Coffee Beans", "Coffee Co", 599, 120, 4.3),
            ("Cooking Oil 1L", "Fortune", 199, 400, 3.8),
            ("Cooking Oil 5L", "Fortune", 899, 100, 3.8),
            ("Salt 1kg", "Annapurna", 49, 500, 4.0),
            ("Biscuits Pack", "Parle", 99, 600, 4.1),
            ("Corn Flakes", "Kellogg", 249, 150, 4.0),
            ("Honey 500g", "Dabur", 399, 80, 4.2),
            ("Peanut Butter", "Jif", 299, 90, 4.1),
            ("Pasta", "Colgate", 149, 120, 3.9),
            ("Noodles", "Maggi", 49, 800, 4.2),
        ],
        "Beauty": [
            ("Face Cream", "HUL", 499, 100, 3.8),
            ("Moisturizer", "Clinique", 799, 60, 4.2),
            ("Sunscreen", "La Shield", 399, 120, 4.0),
            ("Shampoo", "Head and Shoulders", 249, 200, 3.9),
            ("Conditioner", "Pantene", 299, 150, 4.0),
            ("Lip Balm", "Nivea", 149, 300, 4.1),
            ("Face Serum", "The Ordinary", 599, 70, 4.3),
            ("Body Lotion", "Nivea", 249, 250, 3.9),
            ("Face Wash", "Cetaphil", 299, 180, 4.0),
            ("Perfume", "Chanel", 1999, 40, 4.5),
            ("Hair Oil", "Parachute", 299, 150, 4.1),
            ("Toner", "Hada Labo", 399, 90, 4.0),
            ("Face Mask", "Garnier", 199, 160, 3.8),
            ("Makeup Brush Set", "Real Techniques", 499, 50, 4.2),
            ("Nail Polish", "OPI", 499, 45, 4.0),
            ("Hair Straightener", "Philips", 1999, 25, 4.3),
        ],
    }

    def handle(self, *args, **options):
        slug_map = {}
        for name, slug in self.CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=name, defaults={"slug": slug}
            )
            slug_map[name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))
            else:
                if cat.slug != slug:
                    cat.slug = slug
                    cat.save()
                self.stdout.write(f"Category: {name}")

        valid_names = {n for n, _ in self.CATEGORIES}
        for cat in Category.objects.all():
            if cat.name not in valid_names:
                products = Product.objects.filter(category=cat)
                if products.exists():
                    target = slug_map.get(cat.name.title())
                    if target:
                        for p in products:
                            p.category = target
                            p.save()
                cat.delete()

        total = 0
        for cat_name, products in self.PRODUCTS_BY_CATEGORY.items():
            cat = slug_map[cat_name]
            for i, (name, brand, price, stock, rating) in enumerate(products):
                image = f"https://picsum.photos/seed/{cat_name}{i}400/{400}/{400}.jpg"
                existing = Product.objects.filter(name=name, category=cat).first()
                if existing:
                    existing.title = f"{name} by {brand}"
                    existing.price = price
                    existing.stock = stock
                    existing.brand = brand
                    existing.rating = rating
                    existing.image = image
                    existing.is_active = True
                    existing.old_price = round(price * 1.2, 2) if price > 1000 else None
                    existing.discount = 15 if price > 5000 else 10
                    existing.description = f"High quality {name.lower()} from {brand}. Best in class product with premium features and reliable performance."
                    existing.save()
                    total += 1
                else:
                    Product.objects.create(
                        name=name,
                        title=f"{name} by {brand}",
                        description=f"High quality {name.lower()} from {brand}. Best in class product with premium features and reliable performance.",
                        price=price,
                        old_price=round(price * 1.2, 2) if price > 1000 else None,
                        image=image,
                        stock=stock,
                        brand=brand,
                        discount=15 if price > 5000 else 10,
                        rating=rating,
                        category=cat,
                        is_active=True,
                    )
                    total += 1

        self.stdout.write(self.style.SUCCESS(f"\nSeeding complete! {total} products."))
