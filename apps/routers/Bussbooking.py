class busses():
    def __init__(self, capacity:int, name_bus:str):
        self.available_seats = capacity
        self.capacity = capacity
        self.name_bus = name_bus
        self.passangers = []
        
    def add_passanger(self,name:str):
        
        
        if self.available_seats :
            self.passangers.append(name)
            print( f"{name} has been successfully booked at seat {self.capacity - self.available_seats + 1} . Thank you" )
            self.available_seats = self.available_seats - 1
            return True
        else:
            print( f"The bus, {self.name_bus} has no empty seats to book {name}. available seats are {self.available_seats}" )
        return False
        
nganya = busses(4,'trinity')
clients = ["lencer", "dante", "lilian", "mercy", "lolo","danko"]
for x in clients:
    nganya.add_passanger(x)