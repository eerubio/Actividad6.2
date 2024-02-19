"""
Module for managing hotel information and reservations.

Uses JSON file for data storage.

Libraries:
- json: Provides functions for reading and writing JSON data.
- os: Provides functions for interacting with the operating system.
"""
import json
import os
from typing import Dict


class Hotel:
    """
    A class to represent a hotel and manage its information and reservations.
    """

    _reservation_counter = 0

    def __init__(self, filename: str = 'hotels.json'):
        """
        Initializes a Hotel object with the specified hotel data filename.
        """
        self.filename = (filename if filename.endswith('.json')
                         else filename + '.json')

    def _read_hotels_data(self) -> list:
        """
        Reads hotel data from the JSON file.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='UTF-8') as file:
                return json.load(file)
        return []

    def _write_hotels_data(self, data: list):
        """
        Writes hotel data to the JSON file.
        """
        with open(self.filename, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4)

    def create_hotel(self,
                     name: str,
                     location: str,
                     rooms: Dict[str, int]) -> str:
        """
        Creates a new hotel entry in the JSON file.
        """
        hotels_data = self._read_hotels_data()
        hotel_id = len(hotels_data) + 1
        hotel_info = {
            'hotel_id': hotel_id,
            'name': name,
            'location': location,
            'rooms': rooms,
            'reservations': [],
            'customers': []
        }
        hotels_data.append(hotel_info)
        self._write_hotels_data(hotels_data)
        return 'Hotel created'

    def get_customer_id(self, hotel_name: str, customer_name: str) -> int:
        """
        Retrieves the ID of a customer from the hotel's customer list.
        """
        hotels_data = self._read_hotels_data()
        for hotel in hotels_data:
            if hotel['name'] == hotel_name:
                customers = hotel['customers']
                for customer in customers:
                    if customer['customer_name'] == customer_name:
                        return customer['customer_id']
                customer_id = len(customers) + 1
                customers.append({'customer_id': customer_id,
                                  'customer_name': customer_name})
                self._write_hotels_data(hotels_data)
                return customer_id
        return -1

    def delete_hotel(self, hotel_name: str) -> str:
        """
        Deletes a hotel entry from the JSON file.
        """
        hotels_data = self._read_hotels_data()
        for hotel in hotels_data:
            if hotel['name'] == hotel_name:
                hotels_data.remove(hotel)
                self._write_hotels_data(hotels_data)
                return 'Hotel deleted'
        return 'Hotel not found'

    def _find_hotel_by_name(self, hotel_name: str) -> dict:
        """
        Finds a hotel by its name.
        """
        hotels_data = self._read_hotels_data()
        for hotel in hotels_data:
            if hotel['name'] == hotel_name:
                return hotel
        return {}

    def display_hotel_info(self, hotel_name: str) -> dict:
        """
        Displays information about a specific hotel.
        """
        hotel = self._find_hotel_by_name(hotel_name)
        return hotel if hotel else 'Hotel not found'

    def modify_hotel_info(self,
                          hotel_name: str,
                          new_name: str = '',
                          new_location: str = '') -> str:
        """
        Modifies information about a specific hotel.
        """
        hotel = self._find_hotel_by_name(hotel_name)
        if hotel:
            if new_name:
                hotel['name'] = new_name
            if new_location:
                hotel['location'] = new_location
            self._write_hotels_data(self._read_hotels_data())
            return 'Hotel information modified'
        return 'Hotel not found'

    def reserve_room(self, hotel_name: str,
                     customer_name: str,
                     reservation_date: str,
                     room_type: str = 'single') -> str:
        """
        Reserves a room in a specific hotel for a customer.
        """
        hotel = self._find_hotel_by_name(hotel_name)
        if not isinstance(customer_name, str):
            return 'Invalid customer name.'
        if hotel:
            customer_id = self.get_customer_id(hotel_name, customer_name)
            if customer_id == -1:
                return 'Customer not found or could not be created'
            rooms = hotel['rooms']
            if room_type in rooms and rooms[room_type] > 0:
                self._reservation_counter += 1
                reservation_id = self._reservation_counter
                rooms[room_type] -= 1
                hotel['reservations'].append({
                    'id': reservation_id,
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'room_type': room_type,
                    'date': reservation_date
                })
                self._write_hotels_data(self._read_hotels_data())
                return f'{room_type} room reserved for {customer_name}'
            return f'No {room_type} rooms available'
        return f'Hotel {hotel_name} not found'

    def cancel_reservation(self, hotel_name: str, customer_name: str) -> str:
        """
        Cancels a reservation for a customer in a specific hotel.
        """
        hotel = self._find_hotel_by_name(hotel_name)
        if hotel:
            reservations = hotel['reservations']
            for reservation in reservations:
                if reservation['customer_name'] == customer_name:
                    room_type = reservation['room_type']
                    hotel['rooms'][room_type] += 1
                    reservations.remove(reservation)
                    self._write_hotels_data(self._read_hotels_data())
                    return f'Reservation canceled for {customer_name}'
            return f'No reservation found for {customer_name}'
        return f'Hotel {hotel_name} not found'
