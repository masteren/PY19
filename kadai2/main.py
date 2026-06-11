class Monster:
    def __init__(self, name, hp, mp):
        self.__name = name
        self.__hp = hp
        self.__mp = mp

    def show_status(self):
        self.__secret()

    def __secret(self):
        print(self.__name)
        print(self.__hp)
        print(self.__mp)

    def cure(self):
        self.__hp += 100

    def get_name(self):
        return self.__name

monster = Monster('スライム', 10, 5)
monster.show_status()
