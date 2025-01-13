from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), index=True, nullable=False)
    manufacturer = Column(String(100), nullable=False)
    unit = Column(String(50), nullable=False)

    purchases = relationship("Purchase", back_populates="product")

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), index=True, nullable=False)
    address = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=False)
    contact_person = Column(String(100), nullable=False)

    purchases = relationship("Purchase", back_populates="customer")

class Purchase(Base):
    __tablename__ = 'purchases'

    purchase_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    quantity = Column(Float, nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    price_per_unit = Column(Float, nullable=False)

    product = relationship("Product", back_populates="purchases")
    customer = relationship("Customer", back_populates="purchases")
