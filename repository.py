from reservation_model import Reservation
import json
from datetime import datetime

class Repo:
    def __init__(self):
        self.reservations = []
        self.rooms = []  # List of rooms with their capacities
        self.load_data()
        self.assign_rooms()

    def load_data(self):
        data = json.load(open("data.json"))
        # Load reservations
        for rsv in data['Reservations']:
            reservation = Reservation.model_validate(rsv)
            if( datetime.strptime(reservation.checkOut, "%Y-%m-%d") <= datetime.now()):
                pass
            self.reservations.append(reservation)
        # Load rooms (assuming room capacities are stored in the JSON data)
        self.rooms = data['Rooms']  # Example: [{'id': 1, 'capacity': 3}, {'id': 2, 'capacity': 4}]

    def add(self, rsv):
        self.reservations.append(rsv)
        self.assign_rooms()

    def save_data(self):
        dictionary = {
            "Reservations": [resv.to_json() for resv in self.reservations],
            "Rooms": self.rooms  # Save room data if needed
        }
        with open("data.json", "w") as file:
            file.write(json.dumps(dictionary, indent=4))

    def delete(self, rsv):
        self.reservations = [x for x in self.reservations if x != rsv]
        

    def is_available(self, room_schedule, check_in, check_out):
        # Helper function to check room availability based on date ranges
        check_in = datetime.strptime(check_in, "%Y-%m-%d")
        check_out = datetime.strptime(check_out, "%Y-%m-%d")
        for res in room_schedule:
            res_check_in = datetime.strptime(res.checkIn, "%Y-%m-%d")
            res_check_out = datetime.strptime(res.checkOut, "%Y-%m-%d")
            if not (check_out <= res_check_in or check_in >= res_check_out):
                return False
        return True

    def assign_rooms(self):
        # Sort reservations by group size (larger groups first)
        sorted_reservations = sorted(self.reservations, key=lambda x: (-x.people, x.checkIn))

        room_schedules = {room['id']: [] for room in self.rooms}  # Track room bookings

        for reservation in sorted_reservations:
            assigned = False
            for room in sorted(self.rooms, key=lambda x: x['capacity']):
                if room['capacity'] >= reservation.people:
                    # Check if the room is available during the requested period
                    if self.is_available(room_schedules[room['id']], reservation.checkIn, reservation.checkOut):
                        # Assign the room and mark reservation as assigned
                        reservation.room = room['id']
                        room_schedules[room['id']].append(reservation)
                        assigned = True
                        break
            if not assigned:
                reservation.room = -1  # No suitable room found

        self.save_data()

