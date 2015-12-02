from sqlalchemy import Column, Integer, Float, String, DateTime, Enum
from prologue import Base

class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    amount = Column(Float)
    unit = Column(Enum("Count", "Kilogram", "Liter", name="Units"))
    expiration = Column(DateTime)
    picture_id = Column(Integer)

    def __init__(self, label, amount, unit, expiration, picture_id):
        self.label = label
        self.amount = amount
        self.unit = unit
        self.expiration = expiration
        self.picture_id = picture_id

    def as_dict(self):
        return { 'id' : self.id,
                 'label' : self.label,
                 'amount' : self.amount,
                 'unit' : self.unit,
                 'expiration' :
                  { 'year' : self.expiration.year,
                    'month' : self.expiration.month,
                    'day' : self.expiration.day, },
                 'picture_id' : self.picture_id
               }
