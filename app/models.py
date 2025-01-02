from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True)
    manufacturer = Column(String(100))
    unit = Column(String(50))  # единицы измерения
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Customer(Base):
    __tablename__ = 'customer'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True)
    address = Column(String(200))
    phone = Column(String(50))
    contact_person = Column(String(100))
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Purchase(Base):
    __tablename__ = 'purchase'
    
    purchase_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'))
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    quantity = Column(Float)
    delivery_date = Column(DateTime)
    price_per_unit = Column(Float)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
