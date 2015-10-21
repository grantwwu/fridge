from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer)
    unit = Column(String) # Todo: Change to enum
    expiration = Column(DateTime)

    def __init__(name, amount, unit, expiration):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.expiration = expiration

    def as_dict():
        return { 'name' : name,
                 'amount' : amount,
                 'unit' : unit,
                 'expiration' :
                  { 'year' : expiration.year(),
                    'month' : expiration.month(),
                    'day' : expiration.day(), }
               }

