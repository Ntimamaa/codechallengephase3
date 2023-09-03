from requests import session
from lib.Review import Review
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship("Review", back_populates="customer")
    restaurants = relationship("Restaurant", secondary="reviews", back_populates="customers")

    def reviews(self):
        return self.reviews

    def restaurants(self):
        return self.restaurants

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        highest_rating = max(self.reviews, key=lambda review: review.star_rating)
        return highest_rating.restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

