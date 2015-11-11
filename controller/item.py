from sqlalchemy import Column, Integer, String, DateTime, Enum
from app import Base

class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    amount = Column(Float)
    unit = Column(Enum("Count", "Kilogram", "Liters"))
    expiration = Column(DateTime)
    picture_id = Column(Integer)

    def __init__(self, label, amount, unit, expiration, picture_id):
        self.label = label
        self.amount = amount
        self.unit = unit
        self.expiration = expiration
        self.picture_id = picture_id

    def as_dict(self):
        return { 'label' : label,
                 'amount' : amount,
                 'unit' : unit,
                 'expiration' :
                  { 'year' : expiration.year(),
                    'month' : expiration.month(),
                    'day' : expiration.day(), }
               }
