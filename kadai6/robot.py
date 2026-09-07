import random


class Robot:
    def __init__(self, id, name, type):
        self.__id = id
        self.__name = name
        self.__type = type
        self.__secret_items = ("どこでもドア", "タイムマシン", "タケコプター",
                               "スモールライト", "ほんやくコンニャク")

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type

    def help(self):
        return random.choice(self.__secret_items)

    def hello(self):
        print("こんにちは！" + self.__name + "です！")

    def give_dorayaki(self, a):
        if a <= 0:
            print("www")
        elif a <= 4:
            print("xxx")
        elif a <= 9:
            print("yyy")
        else:
            print("zzz")
