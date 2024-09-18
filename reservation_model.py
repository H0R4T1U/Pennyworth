from pydantic import BaseModel

class Reservation(BaseModel):
    name:str
    people:int
    checkIn:str
    checkOut:str
    booking:bool
    room: int | None = -1

    #def __str__(self):
     #   return f"Reservation:{self.name},{self.people} people,\n Perioada: {self.checkIn}->{self.checkOut}\n prin booking:{self.booking}"
    def to_json(self):
        dict = {}
        dict["name"] = self.name
        dict["people"] = self.people
        dict["checkIn"] = self.checkIn
        dict["checkOut"] = self.checkOut
        dict["room"] = self.room
        dict["booking"] = self.booking
        return dict
    
    def __eq__(self,ot: 'Reservation'):
        if self.name != ot.name:
            return False
        if self.people != ot.people:
            return False
        if self.booking != ot.booking:
            return False
        if self.room != ot.room:
            return False
        if self.checkIn != ot.checkIn:
            return False
        if self.checkOut != ot.checkOut:
            return False
        return True
    
    def __lt__(self,ot: 'Reservation'):
        return self.people < ot.people
    
    def __le__(self,ot: 'Reservation'):
        return self.people <= ot.people
    
    def __gt__(self,ot: 'Reservation'):
        return self.people > ot.people
    
    def __ge__(self,ot: 'Reservation'):
        return self.people >= ot.people