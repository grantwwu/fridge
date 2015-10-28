from sqlalchemy import Column, Integer, String, DateTime, Enum, Float

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    amount = Column(Float)
    unit = Column(Enum("Count", "Kilogram", "Liters", name="unit"))
    expiration = Column(DateTime)
    picture_id = Column(Integer)

    def __init__(self, label, amount, unit, expiration, picture_id):
        self.label = label
        self.amount = amount
        self.unit = unit
        self.expiration = expiration
        self.picture_id = picture_id

    def as_dict(self):
        return { 'label' : self.label,
                 'amount' : self.amount,
                 'unit' : self.unit,
                 'expiration' :
                  { 'year' : self.expiration.year,
                    'month' : self.expiration.month,
                    'day' : self.expiration.day, }
               }
