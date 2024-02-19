"""
Module for managing hotel reservations.

Uses JSON file for data storage.

Libraries:
- categories.customer: Provides the Customer class for managing customer
information.
- utilities.json_data_handler: Provides the JSONDataHandler class for handling
JSON data.

Classes:
- Reservation: A class to represent hotel reservations and manage
reservation-related operations.
"""
from customer import Customer
from json_handler import JSONDataHandler


class Reservation(JSONDataHandler):
    """
    A class to represent hotel reservations and manage reservation-related
    operations.

    Attributes:
    - hotel_filename (str): The filename for storing hotel data in JSON format.
    - customer (Customer): An instance of the Customer class for managing
    customer information.

    Methods:
    - create_reservation: Creates a new reservation for a customer in a
    specified hotel.
    - cancel_reservation: Cancels a reservation for a customer in a specified
    hotel.
    """
    def __init__(self, hotel_filename='hotels.json'):
        """
        Initializes a Reservation object with the specified hotel data
        filename.

        Parameters:
        - hotel_filename (str): The filename for storing hotel data in JSON
        format. Defaults to 'hotels.json'.
        """
        super().__init__(hotel_filename)
        self.customer = Customer(hotel_filename)

    def create_reservation(self, hotel_name: str, customer_name: str,
                           reservation_date: str, room_type: str = 'single'):
        """
        Creates a new reservation for a customer in a specified hotel.

        Parameters:
        - hotel_name (str): The name of the hotel.
        - customer_name (str): The name of the customer making the reservation.
        - reservation_date (str): The date of the reservation.
        - room_type (str, optional): The type of room to reserve. Defaults to
        'single'.

        Returns:
        A string indicating the success of the reservation or a message if the
        room type, hotel, or customer was not found or the reservation could
        not be created.
        """
        # Get customer information
        customer_info = self.customer.display_customer_info(hotel_name,
                                                            customer_name)
        # Check if customer information was found
        if isinstance(customer_info, dict):
            # Get the customer ID
            customer_id = customer_info.get('customer_id')
            # Check if the customer ID is None
            if customer_id is None:
                # Create the customer
                return (
                    f'Customer {customer_name} not found or could not be '
                    f'created'
                    )
        # If customer information was not found, return the customer info
        else:
            # Return the customer info
            return customer_info

        # Load hotel data
        hotels_data = self.load_data()
        # Iterate through each hotel in the data
        for hotel_data in hotels_data:
            # Check if the hotel name matches the specified hotel
            if hotel_data['name'] == hotel_name:
                # Check if the room type is available
                if room_type in hotel_data['rooms']:
                    # Check if there are available rooms
                    if hotel_data['rooms'][room_type] > 0:
                        # Create the reservation
                        reservation_id = hotel_data.get('reservation_counter',
                                                        0) + 1
                        # Update the reservation counter
                        hotel_data['reservation_counter'] = reservation_id
                        # Decrement the number of available rooms
                        hotel_data['rooms'][room_type] -= 1
                        # Create the reservation
                        reservation = {
                            'id': reservation_id,
                            'customer_id': customer_id,
                            'customer_name': customer_name,
                            'room_type': room_type,
                            'date': reservation_date
                        }
                        # Add the reservation to the list of reservations
                        hotel_data['reservations'].append(reservation)
                        # Save the updated hotel data
                        self.save_data(hotels_data)
                        # Return a success message
                        return (
                            f'Reservation for {customer_name} created at '
                            f'{hotel_name}'
                        )
                    # If no rooms are available, return an error message
                    return f'No {room_type} rooms available'
                # If the room type is not found, return an error message
                return f'{room_type} room type not found in {hotel_name}'
        # If the hotel is not found, return an error message
        return f'Hotel {hotel_name} not found'

    def cancel_reservation(self, hotel_name: str, customer_name: str):
        """
        Cancels a reservation for a customer in a specified hotel.

        Parameters:
        - hotel_name (str): The name of the hotel.
        - customer_name (str): The name of the customer whose reservation is
        to be canceled.

        Returns:
        A string indicating the success of the cancellation or a message if
        the reservation, hotel, or customer was not found.
        """
        # Load hotel data
        hotels_data = self.load_data()

        # Iterate through each hotel in the data
        for hotel_data in hotels_data:
            if hotel_data['name'] == hotel_name:
                # Check if the hotel is found, retrieve the list of customers
                for reservation in hotel_data['reservations']:
                    # Check if the customer name matches the specified customer
                    if reservation['customer_name'] == customer_name:
                        # If the customer is found, increment the number of
                        # available rooms and remove the reservation
                        room_type = reservation['room_type']
                        # Increment the number of available rooms
                        hotel_data['rooms'][room_type] += 1
                        # Remove the reservation from the list of reservations
                        hotel_data['reservations'].remove(reservation)
                        # Save the updated hotel data
                        self.save_data(hotels_data)
                        # Return a success message
                        return (
                            f'Reservation for {customer_name} cancelled at '
                            f'{hotel_name}'
                            )
                # If the reservation is not found, return an error message
                return (
                    f'No reservation found for {customer_name} in {hotel_name}'
                    )
        # If the hotel is not found, return an error message
        return f'Hotel {hotel_name} not found'
