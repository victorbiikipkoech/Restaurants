from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import desc

Base = declarative_base()
engine = create_engine('sqlite:///restaurant.db')
session = Session(engine)

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        # Find the restaurant with the highest star rating from this customer's reviews
        highest_rated_review = max(self.reviews, key=lambda review: review.star_rating, default=None)
        return highest_rated_review.restaurant if highest_rated_review else None

    def add_review(self, restaurant, rating):
        # Create a new review for the restaurant with the given rating
        new_review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        # Delete all reviews for the given restaurant
        for review in self.reviews:
            if review.restaurant == restaurant:
                session.delete(review)
        session.commit()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    reviews = relationship('Review', back_populates='restaurant')

    @classmethod
    def fanciest(cls):
        # Query the restaurant with the highest price
        return session.query(cls).order_by(desc(cls.price)).first()

    def all_reviews(self):
        # Get a list of formatted strings for all reviews of this restaurant
        review_strings = [
            f"Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars."
            for review in self.reviews
        ]
        return review_strings
    
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars." 
    
# Create tables in the database
Base.metadata.create_all(engine)       