
class Motor:
    def __init__(self, brand, model, fuel, maxspeed, dir):
        self.brand = brand
        self.model = model
        self.fuel = fuel
        self.maxspeed = maxspeed
        if dir < 0 or dir > 4:
            print('liosho')
        self.dir = dir

    def display(self):
        print("brand:" + self.brand)
        print("model:" + self.model)
        print("fuel:" + str(self.fuel))
        print("max speed:" + str(self.maxspeed))
        if self.dir == 1:
            print('napred')
        elif self.dir == 2:
            print('nadqsno')
        elif self.dir == 3:
            print('nalqvo')
        elif self.dir == 4:
            print('nazad')

    def changeDir(self, newDir):
        if newDir < 1 or newDir > 4:
            print('liosho')
        else:
            self.dir = newDir

    def calctime(self, dist):
        t = dist / (self.maxspeed * 0.8)
        print('time: ' + str(t))

m = Motor('BMW', '60', 60, 100, 1)
m.display()
m.changeDir(2)
m.display()
m.calctime(80)

