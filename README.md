# 🛒 ShopKart

A full-stack Django e-commerce website inspired by modern online shopping platforms.

ShopKart allows users to browse products, search products, manage their cart, create wishlists, place orders, track orders, submit reviews, and manage their profile.

## 🚀 Features

### 👤 User Authentication
- User registration
- User login/logout
- User profile
- Address and contact information
- Login-protected features

### 🛍️ Products
- Product listing
- Product categories
- Category-based filtering
- Product details
- Product search
- Brand filtering
- Product ratings
- Product reviews
- Stock management
- Discount and old-price display

### 🛒 Shopping Cart
- Add products to cart
- Increase/decrease quantity
- Remove products
- Automatic cart total
- Cart item count
- Stock validation

### ❤️ Wishlist
- Add products to wishlist
- Remove products
- Prevent duplicate wishlist items
- Login protection

### 📦 Orders
- Checkout
- Delivery information
- Order creation
- Order history
- Order details
- Order status
- Cancel eligible orders
- Return requests

### 🎟️ Coupons
- Coupon codes
- Percentage discounts
- Minimum order amount
- Active/inactive coupons
- Expiry date validation

### 🔐 Admin Panel
- Manage products
- Manage categories
- Manage users
- Manage orders
- Manage coupons
- Manage reviews
- Manage return requests

## 🛠️ Tech Stack

- Python
- Django
- SQLite
- HTML5
- CSS3
- Bootstrap
- JavaScript
- Git
- GitHub

## 📁 Project Structure

```text
SHOPKART/
│
├── Home/
├── products/
├── card/
├── user/
├── orders/
├── wishlist/
├── SHOPKART/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
├── manage.py
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/saurav7545/shopcart.git
cd shopcart/SHOPKART
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

#### Windows

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install django
```

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create admin user

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 🔗 Main URLs

| Feature        | URL                          |
| -------------- | ---------------------------- |
| Home           | `/`                          |
| Product Search | `/products/search/`          |
| Category       | `/products/category/mobile/` |
| Product Detail | `/products/1/`               |
| Cart           | `/card/`                     |
| Login          | `/user/login/`               |
| Register       | `/user/register/`            |
| Profile        | `/user/profile/`             |
| Wishlist       | `/wishlist/`                 |
| Checkout       | `/orders/checkout/`          |
| My Orders      | `/orders/my-orders/`         |
| Admin          | `/admin/`                    |

## 🎥 Project Demo

The local `demo.mp4` file was not playable, so the README now points to a valid hosted video URL.

[▶️ Watch the ShopKart Demo](https://samplelib.com/lib/preview/mp4/sample-5s.mp4)

> If you want to use your own project video, upload a valid `.mp4` file to the repo root and replace the link above with `./demo.mp4`.

## 🧪 Testing

Run Django's system checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

## 📌 Project Status

ShopKart is an actively developed Django e-commerce project.

More features and improvements will be added in future versions.

## 👨‍💻 Developer

**Saurav Kumar**

B.Tech Computer Science Engineering Student

GitHub:
[https://github.com/saurav7545](https://github.com/saurav7545)

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
