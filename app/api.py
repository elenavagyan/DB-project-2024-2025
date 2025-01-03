from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from starlette import status

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

class CustomerBase(BaseModel):
    name: str
    address: str
    phone: str
    contact_person: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int

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

# Product endpoints
@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/", response_model=List[ProductResponse])
def list_products(db: Session, skip: int = 0, limit: int = 100):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# Customer endpoints
@app.post("/customers/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/", response_model=List[CustomerResponse])
def list_customers(db: Session, skip: int = 0, limit: int = 100):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

# Purchase endpoints
@app.post("/purchases/", response_model=PurchaseResponse)
def create_purchase(purchase: PurchaseCreate, db: Session):
    # Verify product and customer exist
    product = db.query(Product).filter(Product.product_id == purchase.product_id).first()
    customer = db.query(Customer).filter(Customer.customer_id == purchase.customer_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_purchase = Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@app.get("/purchases/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(purchase_id: int, db: Session):
    purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

@app.get("/purchases/", response_model=List[PurchaseResponse])
def list_purchases(db: Session, skip: int = 0, limit: int = 100):
    purchases = db.query(Purchase).offset(skip).limit(limit).all()
    return purchases

# Analytics endpoints
@app.get("/analytics/customer-purchases/{customer_id}")
def get_customer_purchases(customer_id: int, db: Session):
    purchases = (db.query(Purchase, Product)
                .join(Product)
                .filter(Purchase.customer_id == customer_id)
                .all())
    return [{
        "product_name": product.name,
        "quantity": purchase.quantity,
        "total_price": purchase.quantity * purchase.price_per_unit,
        "delivery_date": purchase.delivery_date
    } for purchase, product in purchases]

@app.get("/analytics/product-sales/{product_id}")
def get_product_sales(product_id: int, db: Session):
    purchases = db.query(Purchase).filter(Purchase.product_id == product_id).all()
    total_quantity = sum(p.quantity for p in purchases)
    total_revenue = sum(p.quantity * p.price_per_unit for p in purchases)
    return {
        "total_quantity_sold": total_quantity,
        "total_revenue": total_revenue,
        "number_of_purchases": len(purchases)
    }