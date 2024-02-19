"""
This module contains the tests for the Reservation class.
"""
import unittest
import os
from customer import Customer
from reservation import Reservation
from hotel import Hotel


class TestReservation(unittest.TestCase):
    """
    A class to test reservation operations.
    """

    @classmethod
    def setUpClass(cls):
        """
        Sets up the test environment by creating an instance of the Reservation
        class, Customer class, and creating a hotel with customers and
        reservations.
        """
        cls.hotel = Hotel('hotels.json')
        cls.hotel.create_hotel(
            'Luxury Suites',
            'New York City, NY',
            {'single': 3, 'double': 4, 'suite': 6}
        )
        cls.reservation = Reservation('hotels.json')
        cls.customer = Customer('hotels.json')
        cls.customer.create_customer('Luxury Suites', 'Jane Smith')
        cls.customer.create_customer('Luxury Suites', 'Michael Johnson')
        cls.customer.create_customer('Luxury Suites', 'Emma Davis')

    @classmethod
    def tearDownClass(cls):
        """
        Cleans up the test environment by deleting the JSON file if it exists.
        """
        if os.path.exists('hotels.json'):
            os.remove('hotels.json')

    def setUp(self):
        """
        Sets up the test environment.
        """
        self.teardown_called = False

    def tearDown(self):
        """
        Marks that teardown has been called.
        """
        self.teardown_called = True

    def test_create_reservation(self):
        """
        Tests creating a new reservation.
        """
        self.assertEqual(self.reservation.create_reservation(
            'Luxury Suites', 'Jane Smith', '2024-02-20', 'double'),
            'Reservation for Jane Smith created at Luxury Suites')

    def test_create_reservation_no_room_available(self):
        """
        Tests creating a reservation when no rooms of the specified type are
        available.
        """
        self.assertEqual(self.reservation.create_reservation(
            'Luxury Suites', 'Michael Johnson', '2024-02-21', 'pen'),
            'pen room type not found in Luxury Suites')

    def test_create_reservation_hotel_not_found(self):
        """
        Tests creating a reservation for a hotel that does not exist.
        """
        self.assertEqual(self.reservation.create_reservation(
            'Grand Hotel', 'Emma Davis', '2024-02-22', 'single'),
            'Customer Emma Davis not found in Grand Hotel')

    def test_cancel_reservation_success(self):
        """
        Tests canceling a reservation successfully.
        """
        self.reservation.create_reservation('Luxury Suites',
                                            'Jane Smith',
                                            '2024-02-19',
                                            'single')
        self.assertEqual(self.reservation.cancel_reservation(
            'Luxury Suites', 'Jane Smith'),
            'Reservation for Jane Smith cancelled at Luxury Suites')

    def test_cancel_reservation_not_found(self):
        """
        Tests canceling a reservation that does not exist.
        """
        self.assertEqual(self.reservation.cancel_reservation(
            'Luxury Suites', 'Michael Johnson'),
            'No reservation found for Michael Johnson in Luxury Suites')

    def test_cancel_reservation_hotel_not_found(self):
        """
        Tests canceling a reservation in a hotel that does not exist.
        """
        self.assertEqual(self.reservation.cancel_reservation(
            'Grand Hotel', 'Jane Smith'),
            'Hotel Grand Hotel not found')
