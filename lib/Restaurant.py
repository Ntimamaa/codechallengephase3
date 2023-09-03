from requests import session
from sqlalchemy import  Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews = relationship("Review", back_populates="restaurant")
    customers = relationship("Customer", secondary="reviews", back_populates="restaurants")

    def reviews(self):
        return self.reviews

    def customers(self):
        return self.customers

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

