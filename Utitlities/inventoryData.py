import csv
import random

categories_brands = {
    "Dummy": [""],
    "Onion": [""],
    "Apple": [""],
    "Orange": [""],
    "Banana": [""],
    "Tomato": [""],
    "Coke": [""],
    "Fanta": [""],
    "Pepsi": [""],
    "Egg": [""],
    "Milk": [""],
    "Cheese": [""],
    "Nuggets": [""],
    "Chicken": [""],
    "Mutton": [""],
    "Fish": [""],
    "Prawn": [""],
    "Ice": [""],
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

for category, brands in categories_brands.items():
    for brand in brands:
        if category != "Dummy":
            price_per_quantity = get_price()
            stocks_available = random.randint(0, 100)
        else:
            price_per_quantity = 0
            stocks_available = 0

        data.append({
            "brand_category": f"{brand}{category}",
            "price_per_quantity": price_per_quantity,
            "stocks_available": stocks_available
        })

with open('inventoryData.csv', 'w', newline='') as csvfile:
    fieldnames = ['brand_category', 'price_per_quantity', 'stocks_available']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
