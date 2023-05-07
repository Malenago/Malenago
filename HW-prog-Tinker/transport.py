
#----------------- класс, описывающий характеристики транспорта---------------------

class Transport:
    def __init__(self,type,loadcapacity,length,width,height):
        self.type=type
        self.loadcapacity=loadcapacity
        self.length=length
        self.width=width
        self.height=height

    def __str__(self):
        return f"{self.type}: " \
               f"Грузоподъемность {self.loadcapacity} Т," \
               f"Длина {self.length} м," \
               f"Ширина {self.length} м," \
               f"Высота {self.height} м"



#----------- дочерние классы, описывающие виды транспорта, которые есть в компании-----------

class Gazel(Transport):
    def __init__(self,type='Газель',loadcapacity=2,length=3,width=2.1,height=2.8):
        Transport.__init__(self,type,loadcapacity,length,width,height)

class Bachok(Transport):
    def __init__(self,type='Бычок',loadcapacity=3,length=4,width=2.2,height=2):
        Transport.__init__(self,type,loadcapacity,length,width,height)

class Man_10(Transport):
    def __init__(self,type='MAN-10',loadcapacity=10,length=7,width=3,height=2):
        Transport.__init__(self,type,loadcapacity,length,width,height)

class Fyra(Transport):
    def __init__(self,type='Фура',loadcapacity=20,length=14,width=3,height=2.6):
        Transport.__init__(self,type,loadcapacity,length,width,height

