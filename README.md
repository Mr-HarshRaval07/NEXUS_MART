# 🛒 NEXUS MART — Full-Stack E-Commerce Platform

A feature-rich e-commerce web application built with **Django** and **PostgreSQL**, featuring smart product search, AI-powered recommendations, an intelligent chatbot, secure checkout with multiple payment options, and an admin analytics dashboard.

> 🎓 Group Project | Built with Django 5.2 • PostgreSQL • Bootstrap 5 • 

---

## ✨ Features

### 🔍 Smart Search & Autocomplete
- **Live autocomplete** — instant product suggestions as you type (AJAX-powered)
- **Full-text search** using PostgreSQL `SearchVector` with weighted ranking (name = A, description = B) and GIN indexing
- **Multi-filter search** — filter by category, price range, and sorting (low-to-high, high-to-low, newest)
- **Paginated results** — 8 products per page with full pagination support

### 🧠 Similar Product Recommendations
- **Category-based recommendations** on the product detail page — shows 4 related products from the same category
- **Cosine similarity engine** — NumPy-based recommendation system using one-hot encoded category + product specifications to compute feature vectors and rank by cosine similarity

### 🕒 Recently Viewed Products
- Automatically tracks products viewed by authenticated users
- **Deduplication** — viewing the same product again moves it to the top instead of creating duplicates
- **Auto-cleanup** — keeps only the 5 most recent views per user
- Displayed on both **home page** and **search results page**, with optional category filtering

### 🔥 Popular Products
- **View counter** on every product, incremented atomically using Django's `F()` expression (race-condition safe)
- Products ranked by most views and displayed on the home page
- Supports **category-based filtering** — shows popular products within the selected category

### 🛒 Cart & Checkout System
- Add to cart, update quantity (+/-), remove items
- **Stock validation** before checkout — prevents ordering more than available inventory
- **Checkout form** with name, email, phone (Indian mobile validation), and address
- **Atomic transactions** — uses `@transaction.atomic` for data integrity during order placement

### 💳 Payment System
- **Multiple payment methods**: QR Payment, Card Payment, Cash on Delivery (COD)
- **QR payment summary page** with order details and confirmation

### ❤️ Wishlist
- Toggle products in/out of wishlist
- Dedicated **wishlist page** showing all saved products
- Unique constraint per user-product pair

### ⭐ Reviews & Ratings
- Authenticated users can rate products (1–5 stars) and leave comments
- **Average rating** calculated and displayed on product detail page
- One review per user per product (update on re-submit)

### 🤖 AI Chatbot
- Built-in chatbot assistant accessible from every page
- **Natural language understanding** — handles queries like "best phone", "cheap laptop under 50000", "iphone features"
- **Category intelligence** — maps aliases ("mobile" → "Phones & Accessories") to real DB categories
- **Smart responses** — cheapest/expensive/best products, products under a price, product features/specs
- Renders clickable product links in chat responses

### 👤 User Management
- **Registration** with name, email, password
- **Login/Logout** with session management
- **User profile** — editable name, phone (Indian mobile validation), address
- Profile auto-created via Django signals on registration

### 📊 Admin Analytics Dashboard
- **Staff-only** dashboard with sales insights
- **Sales per day** and **orders per day** charts (JSON data for JS rendering)
- **Total revenue** and **total orders** summary
- **Top 5 best-selling products** by quantity sold
- **AI-style insights** — detects if sales are increasing or decreasing

### 🎨 UI/UX
- **Dark/Light mode** toggle with localStorage persistence
- **Responsive design** — works on mobile, tablet, and desktop
- **Glassmorphism** cards with hover animations
- **Fixed bottom bar** for Wishlist and Cart access
- **Image gallery** with carousel and fullscreen zoom modal on product detail page
- Bootstrap 5 + Google Fonts (Inter)

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.2 (Python) |
| **Database** | PostgreSQL with full-text search |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap 5 |
| **Image Handling** | Pillow |
| **Static Files** | WhiteNoise |
| **Deployment** | Gunicorn + WhiteNoise |

---

## 📁 Project Structure

```
NEXUS_MART/
├── config/          # Django settings, root URLs, admin dashboard context
├── products/        # Product, Category, Wishlist, Review, RecentlyViewed models & views
│   └── services/    # Recommendation engine (cosine similarity)
├── search/          # Autocomplete, search results, SearchHistory model
├── orders/          # Cart, checkout, payment, order tracking
├── users/           # Registration, login, profile management
├── chatbot/         # AI chatbot with NLP-style bot logic
├── analytics_app/   # Admin analytics dashboard
├── templates/       # All HTML templates (base, products, orders, users, analytics)
├── static/          # Static assets
├── media/           # Uploaded product images
└── manage.py
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mr-HarshRaval07/NEXUS_HUB.git
cd NEXUS_HUB

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up PostgreSQL database
# Create a database and set the DATABASE_URL environment variable:
set DATABASE_URL=postgres://user:password@localhost:5432/nexus_mart

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (for admin access)
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

---

|

---

## 📄 License

This project was built as a group project for academic purposes.
