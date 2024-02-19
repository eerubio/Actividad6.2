import unittest
import json
import os
from hotel import Hotel


class TestHotelMethods(unittest.TestCase):

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
                "customers": []
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

    def test_create_hotel(self):
        hotel = Hotel(self.test_filename)
        result = hotel.create_hotel("Test Hotel", "City Center", {"single": 5, "double": 10})
        self.assertEqual(result, 'Hotel created')

    def test_get_customer_id_existing_customer(self):
        hotel = Hotel(self.test_filename)
        hotel.create_hotel("Test Hotel", "City Center", {"single": 5, "double": 10})
        hotel.reserve_room("Test Hotel", "John Doe", "2024-03-10", "single")
        result = hotel.get_customer_id("Test Hotel", "John Doe")
        self.assertNotEqual(result, -1)

    def test_get_customer_id_new_customer(self):
        hotel = Hotel(self.test_filename)
        result = hotel.get_customer_id("Nonexistent Hotel", "New Customer")
        self.assertEqual(result, -1)

    def test_delete_hotel_existing_hotel(self):
        hotel = Hotel(self.test_filename)
        hotel.create_hotel("Test Hotel", "City Center", {"single": 5, "double": 10})
        result = hotel.delete_hotel("Test Hotel")
        self.assertEqual(result, 'Hotel deleted')

    def test_delete_hotel_nonexistent_hotel(self):
        hotel = Hotel(self.test_filename)
        result = hotel.delete_hotel("Nonexistent Hotel")
        self.assertEqual(result, 'Hotel not found')

    def test_display_hotel_info_existing_hotel(self):
        hotel = Hotel(self.test_filename)
        hotel.create_hotel("Test Hotel", "City Center", {"single": 5, "double": 10})
        result = hotel.display_hotel_info("Test Hotel")
        self.assertNotEqual(result, 'Hotel not found')

    def test_display_hotel_info_nonexistent_hotel(self):
        hotel = Hotel(self.test_filename)
        result = hotel.display_hotel_info("Nonexistent Hotel")
        self.assertEqual(result, 'Hotel not found')

    def test_modify_hotel_info_existing_hotel(self):
        hotel = Hotel(self.test_filename)
        hotel.create_hotel("Test Hotel", "City Center", {"single": 5, "double": 10})
        result = hotel.modify_hotel_info("Test Hotel", new_name="Modified Hotel")
        self.assertEqual(result, 'Hotel information modified')

    def test_modify_hotel_info_nonexistent_hotel(self):
        hotel = Hotel(self.test_filename)
        result = hotel.modify_hotel_info("Nonexistent Hotel", new_name="Modified Hotel")
        self.assertEqual(result, 'Hotel not found')

    def test_reserve_room_existing_hotel_customer_and_available_rooms(self):
        hotel = Hotel(self.test_filename)
        hotel.create_hotel("Test Hotel", "City Center", {"single": 5, "double": 10})
        hotel.create_hotel("Another Hotel", "Downtown", {"single": 3, "double": 7})
        hotel.reserve_room("Test Hotel", "John Doe", "2024-03-10", "single")
        result = hotel.reserve_room("Another Hotel", "Jane Smith", "2024-03-15", "double")
        self.assertIn('room reserved', result)

    def test_reserve_room_nonexistent_hotel(self):
        hotel = Hotel(self.test_filename)
        result = hotel.reserve_room("Nonexistent Hotel", "John Doe", "2024-03-10", "single")
        self.assertEqual(result, 'Hotel Nonexistent Hotel not found')

    def test_reserve_room_nonexistent_customer(self):
        hotel = Hotel(self.test_filename)
        hotel.create_hotel("Test Hotel", "City Center", {"single": 5, "double": 10})
        result = hotel.reserve_room("Test Hotel", 1, "2024-03-10", "single")
        self.assertEqual(result, 'Invalid customer name.')

    def test_reserve_room_no_available_rooms(self):
        hotel = Hotel(self.test_filename)
        hotel.create_hotel("Test Hotel", "City Center", {"single": 0, "double": 0})
        result = hotel.reserve_room("Test Hotel", "Axel", "2024-03-10", "suit")
        self.assertEqual(result, 'No suit rooms available')


if __name__ == '__main__':
    unittest.main()
