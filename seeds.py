# Import necessary modules and classes
from restaurant import Base, engine, session, Customer, Restaurant, Review

# Add seed data to test the relationships and methods
customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Doe')

restaurant1 = Restaurant(name='Fine Dining', price=5)
restaurant2 = Restaurant(name='Fast Food', price=2)

review1 = Review(customer=customer1, restaurant=restaurant1, star_rating=4)
review2 = Review(customer=customer2, restaurant=restaurant1, star_rating=5)

# Add instances to the session and commit changes
session.add_all([customer1, customer2, restaurant1, restaurant2, review1, review2])
session.commit()

# Test the methods
# Example 1: Print the full name of a customer
print(customer1.full_name())  # Output: John Doe

# Example 2: Find the favorite restaurant of a customer
print(customer2.favorite_restaurant().name)  # Output: Fine Dining

# Example 3: Add a new review for a restaurant
customer1.add_review(restaurant2, 3)

# Example 4: Delete all reviews for a restaurant
customer1.delete_reviews(restaurant1)

# Example 5: Print the full review of a review
print(review1.full_review())  # Output: Review for Fine Dining by John Doe: 4 stars.

# Example 6: Find the fanciest restaurant
print(Restaurant.fanciest().name)  # Output: Fine Dining

# Example 7: Print all reviews for a restaurant
print('\n'.join(restaurant1.all_reviews()))
# Output:
# Review for Fine Dining by John Doe: 4 stars.
# Review for Fine Dining by Jane Doe: 5 stars.
