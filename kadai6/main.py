from robot import Robot

robot = Robot(1, 'ドラえもん', 'ねこ')

# print(robot.get_id())
# print(robot.get_name())
# print(robot.get_type())

# robot.hello()

# # ４つ
# robot.give_dorayaki(0)
# robot.give_dorayaki(1)
# robot.give_dorayaki(5)
# robot.give_dorayaki(10)

# print(robot.help())

robots = []

for i in range(3):
    print(f"第{i+1}個")
    id = input("id=")
    name = input("name=")
    type = input("type=")
    robots.append(Robot(id, name, type))

for r in robots:
    r.hello()
