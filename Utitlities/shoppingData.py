import csv
from datetime import datetime
import random

def generate_random_date():
    year = 2024
    month = 3
    day = random.randint(1, 31)
    return datetime(year, month, day).strftime("%Y-%m-%d")

categories_brands = {
    "Flour": ["Nutrigrain", "Patanjali", "Ashirvad"],
    "Rice": ["IndiaGate", "Patanjali", "Basmati"],
    "Salt": ["Tata", "Patanjali", "Aashirvad"],
    "Sugar": ["Parrys", "Madhur", "HoneyBae"],
    "Pasta": ["Bambino", "Vedaka", "DelMonte"],
    "Noodles": ["Knorr", "Maggie", "Ramen"],
    "Dates": ["Kimia", "Khidri", "Ajwa"],
    "Oil": ["Sunflower", "Saffola", "Fortune"],
    "VegMasala": ["MTR", "Sakthi", "Aachi"],
    "ChickenMasala": ["Eastern", "Mdh", "Everest"],
    "Walnuts": ["Lagom", "Cranberry", "Farmely"],
    "Almonds": ["Mindful", "BrazilNuts", "DailyCrunch"],
    "Biscuit": ["Nutrichoice", "Oreo", "LittleHearts"],
    "Breakfast": ["Oats", "Kellogs", "Chocos"],
    "Detergent": ["Rin", "Tide", "SurfExcel"],
    "Shampoo": ["Dove", "Head&Shoulders", "Sunsilk"],
    "Tea": ["TajMahal", "Lipton", "3Roses"],
    "Coffee": ["Nescafe", "CountryBean", "Continental"],
    "Ketchup": ["Heinz", "Kissan", "Ohms"],
    "Sanitizer": ["LifeBuoy", "Dettol", "Hamam"],
    "Chocolate": ["Amul", "Hershey", "Cadbury"],
    "PopcornMix": ["Popie", "ActII", ""],
    "CatFood": ["Whikas", "PurinaPaw", "FelineFeast"]
}

def get_price():
    return round(random.uniform(10, 100), 2)

data = []

for _ in range(5000):
    date = generate_random_date()
    category = random.choice(list(categories_brands.keys()))
    brand = random.choice(categories_brands[category])
    quantity_sold = random.randint(1, 100)
    price_per_quantity = get_price()
    total_price = quantity_sold * price_per_quantity

    data.append({
        "date": date,
        "product_name": f"{brand}{category}",
        "category": category,
        "brand": brand,
        "quantity_sold": quantity_sold,
        "price_per_quantity": price_per_quantity,
        "total_price": total_price
    })

with open('shoppingData.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'product_name', 'category', 'brand', 'quantity_sold', 'price_per_quantity', 'total_price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in data:
        writer.writerow(entry)
