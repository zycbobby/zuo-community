__author__ = 'Administrator'

class Car(object):
    def __init__(self,name):
        self.name=name
        pass

    def showName(self):
        print self.name

    @classmethod
    def ReadCar(cls,name):
        return Car(name)


if __name__=='__main__':
    c=Car.ReadCar('Benz')
    d=Car('vw')
    c.showName()
    d.showName()