import random
from datetime import datetime, timedelta

def get_random_company_name():
    prefixes = ["Tech", "Global", "Super", "Mega", "Pro", "Smart", "Elite", "Prime", "First", "Best"]
    suffixes = ["Corp", "Systems", "Solutions", "Industries", "Group", "Partners", "International", "Ltd", "Inc", "Co"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def get_random_manufacturer():
    manufacturers = [
        "TechPro Manufacturing",
        "GlobalTech Industries",
        "Innovative Solutions",
        "Quality Producers",
        "Premium Products",
        "Standard Manufacturing",
        "Elite Industries",
        "Professional Products",
        "Advanced Systems",
        "Core Manufacturing"
    ]
    return random.choice(manufacturers)

def get_random_unit():
    units = ["piece", "kg", "liter", "meter", "set", "box", "pack", "ton", "pair", "bundle"]
    return random.choice(units)

def get_random_product_name():
    products = [
        "Laptop Computer",
        "Office Chair",
        "Desk Lamp",
        "Printer Paper",
        "Coffee Maker",
        "Filing Cabinet",
        "Whiteboard",
        "Phone Charger",
        "USB Drive",
        "Wireless Mouse"
    ]
    return random.choice(products)

def get_random_phone():
    return f"+7({random.randint(900,999)}){random.randint(1000000,9999999)}"

def get_random_address():
    streets = ["Main", "Park", "Lake", "Hill", "Forest", "River", "Mountain", "Valley", "Spring", "Meadow"]
    cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan", "Nizhny Novgorod", "Samara"]
    return f"{random.randint(1,100)} {random.choice(streets)} St., {random.choice(cities)}"

def get_random_person_name():
    first_names = ["Ivan", "Alexander", "Dmitry", "Mikhail", "Sergey", "Anna", "Elena", "Maria", "Olga", "Natalia"]
    last_names = ["Ivanov", "Petrov", "Sidorov", "Smirnov", "Kuznetsov", "Popov", "Sokolov", "Lebedev", "Kozlov"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def get_random_quantity():
    return round(random.uniform(1, 1000), 2)

def get_random_price():
    return round(random.uniform(10, 10000), 2)

def get_random_date(start_date=None):
    if start_date is None:
        start_date = datetime.now() - timedelta(days=365)
    max_days = (datetime.now() + timedelta(days=30) - start_date).days
    days_to_add = random.randint(0, max_days)
    return start_date + timedelta(days=days_to_add)
