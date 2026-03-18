import re
from products.models import Product

BASE_URL = "http://127.0.0.1:8000"


def product_link(product):
    return f'<a href="{BASE_URL}/product/{product.id}/" target="_blank">View product</a>'


# -------- SMART HELPERS -------- #

CHEAP_WORDS = ["cheap", "cheapest", "lowest", "budget", "low price"]
EXPENSIVE_WORDS = ["expensive", "costliest", "highest", "premium"]
BEST_WORDS = ["best", "top", "recommended", "suggest"]
FEATURE_WORDS = ["feature", "spec", "details", "info", "about"]


# CATEGORY INTELLIGENCE (REAL DB CATEGORY NAMES)
CATEGORY_ALIASES = {
    "Phones & Accessories": ["mobile", "mobiles", "phone", "phones", "smartphone"],
    "Laptops & Computers": ["laptop", "laptops", "macbook", "notebook"],
    "Home Appliances": ["fridge", "refrigerator"],
    "Kitchen Appliances": ["mixer", "grinder", "air fryer", "fryer"],
}


def extract_category(msg):
    # 1️⃣ Direct match with database category names
    categories = Product.objects.values_list("category__name", flat=True).distinct()

    for cat in categories:
        if cat and cat.lower() in msg:
            return cat

    # 2️⃣ Alias match (returns REAL DB category)
    for real_cat, aliases in CATEGORY_ALIASES.items():
        for word in aliases:
            if word in msg:
                return real_cat

    return None




def extract_price(msg):
    numbers = re.findall(r'\d+', msg)
    if numbers:
        return int(numbers[0])
    return None


# -------- MAIN BOT -------- #

def get_bot_reply(message):
    msg = message.lower()

    queryset = Product.objects.all()

    category = extract_category(msg)
    price_limit = extract_price(msg)

    # Apply category filter
    if category:
        queryset = queryset.filter(category__name__icontains=category)

    # Apply price filter
    if price_limit and any(x in msg for x in ["under", "below", "less than"]):
        queryset = queryset.filter(price__lte=price_limit)

    # =====================================
    # 💰 CHEAPEST PRODUCTS
    # =====================================
    if any(word in msg for word in CHEAP_WORDS):
        product = queryset.order_by("price").first()
        if product:
            return (
                f"💰 Cheapest {category if category else 'product'} is {product.name} at ₹{product.price}\n"
                f"👉 {product_link(product)}"
            )
        return "No products found."

    # =====================================
    # 💎 MOST EXPENSIVE PRODUCTS
    # =====================================
    if any(word in msg for word in EXPENSIVE_WORDS):
        product = queryset.order_by("-price").first()
        if product:
            return (
                f"💎 Most expensive {category if category else 'product'} is {product.name} at ₹{product.price}\n"
                f"👉 {product_link(product)}"
            )
        return "No products found."

    # =====================================
    # ⭐ BEST / SUGGESTED PRODUCTS
    # =====================================
    if any(word in msg for word in BEST_WORDS):
        products = queryset.order_by("-price")[:3]  # simple logic: higher price = premium
        if products:
            reply = f"⭐ Here are some best {category if category else 'products'}:\n"
            for p in products:
                reply += f"{p.name} – ₹{p.price}\n👉 {product_link(p)}\n"
            return reply
        return "No products found."

    # =====================================
    # 🛒 PRODUCTS UNDER PRICE
    # =====================================
    if price_limit and any(x in msg for x in ["under", "below", "less than"]):
        products = queryset.order_by("price")[:5]
        if products:
            reply = f"🛒 Products under ₹{price_limit}:\n"
            for p in products:
                reply += f"{p.name} – ₹{p.price}\n👉 {product_link(p)}\n"
            return reply
        return "No products in that range."

    # =====================================
    # 📋 PRODUCT FEATURES / DETAILS
    # =====================================
    if any(word in msg for word in FEATURE_WORDS):
        # try to find product name inside sentence
        for product in Product.objects.all():
            if product.name.lower() in msg:
                return (
                    f"📋 Features of {product.name}:\n"
                    f"Price: ₹{product.price}\n"
                    f"Category: {product.category.name}\n"
                    f"👉 {product_link(product)}"
                )

    # =====================================
    # 🔎 NATURAL SENTENCE PRODUCT SEARCH
    # =====================================
    for product in Product.objects.all():
        if product.name.lower() in msg:
            return (
                f"Found {product.name} at ₹{product.price}\n"
                f"👉 {product_link(product)}"
            )

    # =====================================
    # 🤖 SMART CATEGORY SUGGESTION
    # =====================================
    if category:
        products = queryset.order_by("price")[:3]
        if products:
            reply = f"🤖 Some {category} you may like:\n"
            for p in products:
                reply += f"{p.name} – ₹{p.price}\n👉 {product_link(p)}\n"
            return reply

    # Greeting
    if any(x in msg for x in ["hi", "hello", "hey"]):
        return (
            "Hi 👋 I can help you find products!\n"
            "Try:\n"
            "• best phone\n"
            "• cheap laptop under 50000\n"
            "• iphone features\n"
            "• suggest mobiles"
        )

    return "🤖 I didn't understand. Try: best phone, cheap laptop, or iphone features."
