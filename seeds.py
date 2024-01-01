from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.restaurant import Base, Restaurant
from models.customer import Customer
from models.review import Review

engine = create_engine('sqlite:///my_database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Sample data
restaurant1 = Restaurant(name='Restaurant A', price=3)
restaurant2 = Restaurant(name='Restaurant B', price=4)

customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Smith')

review1 = Review(restaurant=restaurant1, customer=customer1, star_rating=4)
review2 = Review(restaurant=restaurant2, customer=customer1, star_rating=5)

# Add instances to the session and commit
session.add_all([restaurant1, restaurant2, customer1, customer2, review1, review2])
session.commit()

# Query examples
restaurant_reviews = session.query(Restaurant).filter_by(name='Restaurant A').first().reviews
customer_restaurants = session.query(Customer).filter_by(first_name='John').first().restaurants

# Print some information
for review in restaurant_reviews:
    print(review.full_review())

for restaurant in customer_restaurants:
    print(restaurant.name)
