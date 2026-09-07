class Car:
    def __init__(self, type):
        self.__type = type

    def show_type(self):
        print(self.__type)


car = Car('セダン')
# car.show_type()

car2 = Car('ban')
car3 = Car('mini ban')
car4 = Car('k')

# そもそも個別の変数で持つのではなく、リスト等のデータ群の形で保持べき

cars = []

cars.append(Car('セダン'))
cars.append(Car('ban'))
cars.append(Car('mini ban'))
cars.append(Car('k'))

for car in cars:
    car.show_type()

# cars[0].show_type()
# cars[1].show_type()
# cars[2].show_type()
# cars[3].show_type()

# おまけ ~無理くりバージョン~
for car in [car, car2, car3, car4]:
    car.show_type()
