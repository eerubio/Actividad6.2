import unittest
import json
import os
from customer import Customer


class TestHotelAndCustomerMethods(unittest.TestCase):

    def setUp(self):
        # Create a fixed hotels.json file for testing
        self.test_filename = 'hotels.json'
        self.initialize_test_data()

    def tearDown(self):
        # Clean up the test data after testing
        os.remove(self.test_filename)

    def initialize_test_data(self):
        # Initialize the hotels.json file with test data
        test_data = [
            {
                "hotel_id": 1,
                "name": "Test Hotel",
                "location": "City Center",
                "rooms": {"single": 5, "double": 10},
                "reservations": [],
                "customers": [
                    {"customer_id": 1, "customer_name": "John Doe"}
                ]
            },
            {
                "hotel_id": 2,
                "name": "Another Hotel",
                "location": "Downtown",
                "rooms": {"single": 3, "double": 7},
                "reservations": [],
                "customers": []
            }
        ]
        with open(self.test_filename, 'w', encoding='UTF-8') as file:
            json.dump(test_data, file, indent=4)

    def test_create_customer_existing_hotel(self):
        customer = Customer(self.test_filename)
        result = customer.create_customer("Test Hotel", "Jane Smith")
        self.assertEqual(result, 'Customer Jane Smith created for Test Hotel')

    def test_create_customer_nonexistent_hotel(self):
        customer = Customer(self.test_filename)
        result = customer.create_customer("Nonexistent Hotel", "John Doe")
        self.assertEqual(result, 'Customer John Doe not created. Hotel Nonexistent Hotel not found')

    def test_delete_customer_existing_customer(self):
        customer = Customer(self.test_filename)
        result = customer.delete_customer("Test Hotel", "John Doe")
        self.assertEqual(result, 'Customer John Doe deleted')

    def test_delete_customer_nonexistent_customer(self):
        customer = Customer(self.test_filename)
        result = customer.delete_customer("Test Hotel", "Nonexistent Customer")
        self.assertEqual(result, 'Customer Nonexistent Customer not found in Test Hotel')

    def test_display_customer_info_existing_customer(self):
        customer = Customer(self.test_filename)
        result = customer.display_customer_info("Test Hotel", "John Doe")
        self.assertNotEqual(result, 'Customer John Doe not found in Test Hotel')

    def test_display_customer_info_nonexistent_customer(self):
        customer = Customer(self.test_filename)
        result = customer.display_customer_info("Test Hotel", "Nonexistent Customer")
        self.assertEqual(result, 'Customer Nonexistent Customer not found in Test Hotel')

    def test_modify_customer_info_existing_customer(self):
        customer = Customer(self.test_filename)
        result = customer.modify_customer_info("Test Hotel", "John Doe", "John Smith")
        self.assertEqual(result, 'Customer name updated from John Doe to John Smith')

    def test_modify_customer_info_nonexistent_customer(self):
        customer = Customer(self.test_filename)
        result = customer.modify_customer_info("Test Hotel", "Nonexistent Customer", "John Smith")
        self.assertEqual(result, 'Customer Nonexistent Customer not found in Test Hotel')


if __name__ == '__main__':
    unittest.main()
