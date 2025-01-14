import random
from datetime import datetime, timedelta
from typing import Dict, Any, Callable
import inspect
from sqlalchemy.orm import Session
from models import Product, Customer, Purchase

# Functions for generating random data

def get_random_company_name() -> str:
    prefixes = ["Tech", "Global", "Super", "Mega", "Pro", "Smart", "Elite", "Prime", "First", "Best"]
    suffixes = ["Corp", "Systems", "Solutions", "Industries", "Group", "Partners", "International", "Ltd", "Inc", "Co"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def get_random_manufacturer() -> str:
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

def get_random_unit() -> str:
    units = ["piece", "kg", "liter", "meter", "set", "box", "pack", "ton", "pair", "bundle"]
    return random.choice(units)

def get_random_product_name() -> str:
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

def get_random_phone() -> str:
    return f"+7({random.randint(900, 999)}){random.randint(1000000, 9999999)}"

def get_random_address() -> str:
    streets = ["Main", "Park", "Lake", "Hill", "Forest", "River", "Mountain", "Valley", "Spring", "Meadow"]
    cities = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan", "Nizhny Novgorod", "Samara"]
    return f"{random.randint(1, 100)} {random.choice(streets)} St., {random.choice(cities)}"

def get_random_person_name() -> str:
    first_names = ["Ivan", "Alexander", "Dmitry", "Mikhail", "Sergey", "Anna", "Elena", "Maria", "Olga", "Natalia"]
    last_names = ["Ivanov", "Petrov", "Sidorov", "Smirnov", "Kuznetsov", "Popov", "Sokolov", "Lebedev", "Kozlov"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def get_random_quantity() -> int:
    return round(random.uniform(1, 1000), 2)

def get_random_price() -> float:
    return round(random.uniform(10, 10000), 2)

def get_random_date(start_date: datetime = None) -> datetime:
    if start_date is None:
        start_date = datetime.now() - timedelta(days=365)
    max_days = (datetime.now() + timedelta(days=30) - start_date).days
    days_to_add = random.randint(0, max_days)
    return start_date + timedelta(days=days_to_add)


def generate_random_products(count: int, db: Session):
    for _ in range(count):
        name = get_random_product_name()
        manufacturer = get_random_manufacturer()
        unit = get_random_unit()

        product = Product(name=name, manufacturer=manufacturer, unit=unit)
        db.add(product)

    db.commit()
    return f"{count} random products generated successfully."


def generate_random_customers(count: int, db: Session):
    for _ in range(count):
        name = get_random_person_name()
        address = get_random_address()
        phone = get_random_phone()
        contact_person = get_random_person_name()

        customer = Customer(name=name, address=address, phone=phone, contact_person=contact_person)
        db.add(customer)

    db.commit()
    return f"{count} random customers generated successfully."


def generate_random_purchases(count: int, db: Session):
    products = db.query(Product).all()
    customers = db.query(Customer).all()

    if not products or not customers:
        return "Error: There must be at least one product and one customer in the database to generate purchases."

    for _ in range(count):
        product = random.choice(products)
        customer = random.choice(customers)
        quantity = get_random_quantity()
        delivery_date = get_random_date()
        price_per_unit = get_random_price()

        purchase = Purchase(
            product_id=product.product_id,
            customer_id=customer.customer_id,
            quantity=quantity,
            delivery_date=delivery_date,
            price_per_unit=price_per_unit,
        )
        db.add(purchase)

    db.commit()
    return f"{count} random purchases generated successfully."


# Conversion function to datetime
def to_datetime(input_str: str) -> datetime:
    try:
        return datetime.strptime(input_str, "%Y-%m-%d_%H:%M:%S")
    except ValueError as err:
        raise ValueError(f"Invalid date/time format: {input_str}") from err



# Command Mapping
method_dict = {
    "product": {
        "create": lambda name, manufacturer, unit, db: create_product(name, manufacturer, unit, db),
        "get": lambda product_id, db: get_product(product_id, db),
        "get-all": lambda db, *args: get_all_products(db),
        "delete": lambda product_id, db: delete_product(product_id, db),
        "delete-all": lambda db: delete_all_products(db),
        "generate": lambda count, db: generate_random_products(int(count), db),
    },
    "customer": {
        "create": lambda name, address, phone, contact_person, db: create_customer(name, address, phone, contact_person, db),
        "get": lambda customer_id, db: get_customer(customer_id, db),
        "get-all": lambda db, *args: get_all_customers(db),
        "delete": lambda customer_id, db: delete_customer(customer_id, db),
        "delete-all": lambda db: delete_all_customers(db),
        "generate": lambda count, db: generate_random_customers(int(count), db),
    },
    "purchase": {
        "create": lambda product_id, customer_id, quantity, delivery_date, price_per_unit, db: create_purchase(product_id, customer_id, quantity, delivery_date, price_per_unit, db),
        "get": lambda purchase_id, db: get_purchase(purchase_id, db),
        "get-all": lambda db, *args: get_all_purchases(db),
        "delete": lambda purchase_id, db: delete_purchase(purchase_id, db),
        "delete-all": lambda db: delete_all_purchases(db),
        "generate": lambda count, db: generate_random_purchases(int(count), db),
    },
}





# ------------------------------
# 🛠️ Product Functions
# ------------------------------
def create_product(name, manufacturer, unit, db: Session):
    product = Product(name=name, manufacturer=manufacturer, unit=unit)
    db.add(product)
    db.commit()
    db.refresh(product)
    return f"Product created: {product.product_id}, {product.name}, {product.manufacturer}, {product.unit}"

def get_product(product_id, db: Session):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return f"Product with ID {product_id} not found."
    return f"Product: {product.product_id}, {product.name}, {product.manufacturer}, {product.unit}"

def get_all_products(db: Session):
    products = db.query(Product).all()
    return [f"{product.product_id}: {product.name}, {product.manufacturer}, {product.unit}" for product in products]

def delete_product(product_id, db: Session):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return f"Product with ID {product_id} not found."
    db.delete(product)
    db.commit()
    return f"Product with ID {product_id} deleted."

def delete_all_products(db: Session):
    products = db.query(Product).all()

    if not products:
        return "No products to delete."

    db.query(Product).delete()
    db.commit()
    return "All products deleted successfully."


# ------------------------------
# 🛠️ Customer Functions
# ------------------------------
def create_customer(name, address, phone, contact_person, db: Session):
    customer = Customer(name=name, address=address, phone=phone, contact_person=contact_person)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return f"Customer created: {customer.customer_id}, {customer.name}, {customer.address}, {customer.phone}"

def get_customer(customer_id, db: Session):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        return f"Customer with ID {customer_id} not found."
    return f"Customer: {customer.customer_id}, {customer.name}, {customer.address}, {customer.phone}"

def get_all_customers(db: Session):
    customers = db.query(Customer).all()
    return [f"{customer.customer_id}: {customer.name}, {customer.address}, {customer.phone}" for customer in customers]

def delete_customer(customer_id: int, db: Session):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

    if not customer:
        return f"Customer with ID {customer_id} not found."

    db.delete(customer)
    db.commit()
    return f"Customer with ID {customer_id} deleted successfully."

def delete_all_customers(db: Session):
    customers = db.query(Customer).all()

    if not customers:
        return "No customers to delete."

    db.query(Customer).delete()
    db.commit()
    return f"All customers deleted successfully."



# ------------------------------
# 🛠️ Purchase Functions
# ------------------------------
def create_purchase(product_id, customer_id, quantity, delivery_date, price_per_unit, db: Session):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

    if not product:
        return f"Product with ID {product_id} not found."
    if not customer:
        return f"Customer with ID {customer_id} not found."

    purchase = Purchase(
        product_id=product_id,
        customer_id=customer_id,
        quantity=quantity,
        delivery_date=delivery_date,
        price_per_unit=price_per_unit
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return f"Purchase created: {purchase.purchase_id}, Product ID: {purchase.product_id}, Customer ID: {purchase.customer_id}, Quantity: {purchase.quantity}, Delivery Date: {purchase.delivery_date}, Price per Unit: {purchase.price_per_unit}"

def get_purchase(purchase_id, db: Session):
    purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()
    if not purchase:
        return f"Purchase with ID {purchase_id} not found."
    return f"Purchase: {purchase.purchase_id}, Product ID: {purchase.product_id}, Customer ID: {purchase.customer_id}, Quantity: {purchase.quantity}, Delivery Date: {purchase.delivery_date}, Price per Unit: {purchase.price_per_unit}"

def get_all_purchases(db: Session):
    purchases = db.query(Purchase).all()
    return [
        f"{purchase.purchase_id}: Product ID: {purchase.product_id}, Customer ID: {purchase.customer_id}, Quantity: {purchase.quantity}, Delivery Date: {purchase.delivery_date}, Price per Unit: {purchase.price_per_unit}"
        for purchase in purchases
    ]

def delete_purchase(purchase_id, db: Session):
    purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()
    if not purchase:
        return f"Purchase with ID {purchase_id} not found."
    db.delete(purchase)
    db.commit()
    return f"Purchase with ID {purchase_id} deleted."

def delete_all_purchases(db: Session):
    purchases = db.query(Purchase).all()

    if not purchases:
        return "No purchases to delete."

    db.query(Purchase).delete()
    db.commit()
    return f"All purchases deleted successfully."



# Command Parsing Functions
def parse_command(command: str) -> Dict[str, Any]:
    try:
        args = command.split()
        if len(args) < 2:
            return {"valid": False}

        entity, action = args[0], args[1]
        if entity not in method_dict or action not in method_dict[entity]:
            return {"valid": False}

        return {
            "valid": True,
            "entity": entity,
            "action": action,
            "args": args[2:],
            "method": method_dict[entity][action]
        }
    except Exception:
        return {"valid": False}

def print_unknown():
    print("Unknown/invalid command. Available commands:")
    print("product: create, get, get-all, update, delete, delete-all, generate")
    print("customer: create, get, get-all, update, delete, delete-all, generate")
    print("purchase: create, get, get-all, update, delete, delete-all, generate")
    print("query: 1 (products by manufacturer), 2 (customer purchases), 3 (update prices), 4 (sales by product)")

async def invoke(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        # If the function is async, await it
        return await func(*args, **kwargs)
    else:
        # If the function is sync, call it normally
        return func(*args, **kwargs)
