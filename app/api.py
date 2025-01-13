from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from models import Product, Customer, Purchase
from session import get_db

app = FastAPI()

# Pydantic models for request/response
class ProductBase(BaseModel):
    name: str
    manufacturer: str
    unit: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int

    model_config = ConfigDict(from_attributes=True)

class CustomerBase(BaseModel):
    name: str
    address: str
    phone: str
    contact_person: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int

    model_config = ConfigDict(from_attributes=True)

class PurchaseBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: float
    delivery_date: datetime
    price_per_unit: float

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseResponse(PurchaseBase):
    purchase_id: int

    model_config = ConfigDict(from_attributes=True)

# Product endpoints
@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/", response_model=List[ProductResponse])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# Customer endpoints
@app.post("/customers/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/", response_model=List[CustomerResponse])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

# Purchase endpoints
@app.post("/purchases/", response_model=PurchaseResponse)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == purchase.product_id).first()
    customer = db.query(Customer).filter(Customer.customer_id == purchase.customer_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db_purchase = Purchase(**purchase.model_dump())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@app.get("/purchases/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

@app.get("/purchases/", response_model=List[PurchaseResponse])
def list_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchases = db.query(Purchase).offset(skip).limit(limit).all()
    return purchases


# SELECT with Multiple Conditions (WHERE)

@app.get("/products/filter/")
def filter_products(
    manufacturer: str, 
    unit: str, 
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.manufacturer == manufacturer,
        Product.unit == unit
    ).all()
    return products

# JOIN Query

@app.get("/purchases/details/")
def get_purchase_details(db: Session = Depends(get_db)):
    purchases = (
        db.query(Purchase, Product, Customer)
        .join(Product, Purchase.product_id == Product.product_id)
        .join(Customer, Purchase.customer_id == Customer.customer_id)
        .all()
    )

    result = [
        {
            "purchase_id": purchase.Purchase.purchase_id,
            "product_name": purchase.Product.name,
            "customer_name": purchase.Customer.name,
            "quantity": purchase.Purchase.quantity,
            "delivery_date": purchase.Purchase.delivery_date,
            "price_per_unit": purchase.Purchase.price_per_unit
        }
        for purchase in purchases
    ]

    return result

# UPDATE with Non-Trivial Condition

@app.put("/purchases/update-price/{purchase_id}")
def update_price(purchase_id: int, new_price: float, db: Session = Depends(get_db)):
    purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()

    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")

    if purchase.quantity > 10:  # Non-trivial condition
        purchase.price_per_unit = new_price
        db.commit()
        db.refresh(purchase)
        return {"message": "Price updated successfully", "purchase_id": purchase_id}

    return {"message": "Price not updated. Quantity is too low."}

# GROUP BY Query

from sqlalchemy.sql import func

@app.get("/purchases/group-by-product/")
def group_purchases_by_product(db: Session = Depends(get_db)):
    grouped_purchases = (
        db.query(Purchase.product_id, func.sum(Purchase.quantity).label("total_quantity"))
        .group_by(Purchase.product_id)
        .all()
    )

    result = [
        {
            "product_id": product_id,
            "total_quantity": total_quantity
        }
        for product_id, total_quantity in grouped_purchases
    ]

    return result

# Sorting Query Results

@app.get("/customers/sorted/")
def get_sorted_customers(
    sort_by: str = "name", 
    db: Session = Depends(get_db)
):
    valid_sort_fields = {
        "name": Customer.name,
        "address": Customer.address,
        "phone": Customer.phone
    }

    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    customers = db.query(Customer).order_by(valid_sort_fields[sort_by]).all()
    return customers
