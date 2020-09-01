import random
import numpy


def clear():
    print('\n')


class MapGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height


g = MapGrid(50, 15)
walls = []
day = 0
time = 0



def draw_grid(graph, width=2):
    clear()
    print_toolbar()
    for y in range(graph.height):
        for x in range(graph.width):
            if (x, y) in walls:
                print("%%-%ds" % width % '#', end="")
            elif (x, y) == (blecks.x, blecks.y):
                print("%%-%ds" % width % 'B', end="")
            elif (x, y) in npc_locations.values():
                print("%%-%ds" % width % 'H', end="")
            elif (x, y) in (get_item_locations()):
                print("%%-%ds" % width % '+', end="")
            else:
                print("%%-%ds" % width % '.', end="")
        print()


def build_wall(origin_xy, dir_length, axis):
    global walls
    if axis == 'x':
        i = origin_xy[0]
        if dir_length > 0:
            while i < dir_length + origin_xy[0]:
                walls.append((i, origin_xy[1]))
                i += 1
        elif dir_length < 0:
            while i > dir_length + origin_xy[0]:
                walls.append((i, origin_xy[1]))
                i -= 1
    elif axis == 'y':
        i = origin_xy[1]
        if dir_length > 0:
            while i < dir_length + origin_xy[1]:
                walls.append((origin_xy[0], i))
                i += 1
        elif dir_length < 0:
            while i > dir_length + origin_xy[1]:
                walls.append((origin_xy[0], i))
                i -= 1


npc_locations = {}
existing_items = []

def get_item_locations():
    global existing_items
    locations = []
    for x in existing_items:
        locations.append(x[1])
    return locations




def npc_interactions(name):
    if str(name) == 'tamel':
        normal_actions(str(name) + ': "welcome to town, blecks"')
    else:
        normal_actions(str(name) + ': "excuse me"')


def message(content):
    draw_grid(g)
    print(str(content))


def input_message(content):
    draw_grid(g)
    input(str(content))


class Person:
    instances = []

    def __init__(self, name, x=1, y=1):
        self.name = str(name)
        self.race = 'human'
        self.hp = 10
        self.speed = 10
        self.combat_skill = 1.0
        self.gold = 100
        self.inventory = ['paper', 'dildo', 'bucket']
        self.x = x
        self.y = y
        self.__class__.instances.append(self)
        self.move_probability = 70
        if self.name != 'blecks':
            npc_locations[self.name] = (self.x, self.y)

    @classmethod
    def move_npcs(cls):
        for instance in cls.instances:
            if instance.name != 'blecks':
                move_roll = random.randint(1, 100)
                if move_roll <= instance.move_probability:
                    dir_roll = random.randint(1, 4)
                    if dir_roll == 1:
                        direction = 'd'
                    elif dir_roll:
                        direction = 'a'
                    elif dir_roll == 3:
                        direction = 'w'
                    elif dir_roll == 4:
                        direction = 's'
                    instance.move(direction)

    def move(self, direction):
        global time
        global g
        if direction == 'd':
            destination = (self.x + 1, self.y)
        elif direction == 'a':
            destination = (self.x - 1, self.y)
        elif direction == 'w':
            destination = (self.x, self.y - 1)
        elif direction == 's':
            destination = (self.x, self.y + 1)

        if destination in walls:
            if self.name == 'blecks':
                normal_actions('ouch')
        elif destination in npc_locations.values():
            if self.name == 'blecks':
                for x in npc_locations.items():
                    if x[1] == destination:
                        target = x[0]
                        npc_interactions(target)
        else:
            self.x = destination[0]
            self.y = destination[1]
            if self.name == 'blecks':
                messages = []
                time += self.speed
                Person.move_npcs()
                items_here = []
                for x in existing_items:
                    if x[1] == (self.x, self.y):
                        items_here.append(str(x[0]))
                if len(items_here) > 0:
                    i = 1
                    for x in items_here:
                        messages.append(str(i) + '. ' + str(x))
                        i += 1
                normal_actions(str(messages))

            else:
                npc_locations[self.name] = (self.x, self.y)


    def item_actions(self, item):
        actions = ['drop', 'place/give', 'hit with']
        i = 1
        for x in actions:
            print(str(i) + '. ' + x)
            i += 1

        player_choice = input('x = back\n')
        if player_choice.isnumeric() == True:
            if actions[(int(player_choice) - 1)] == 'drop':
                existing_items.append((str(item), (blecks.x, blecks.y)))
                self.inventory.remove(str(item))
                normal_actions(f"you drop the {item}")
            if actions[(int(player_choice) - 1)] == 'place/give':
                dir = input('what direction? ')

                if dir == 'd':
                    destination = (blecks.x + 1, blecks.y)
                elif dir == 'a':
                    destination = (blecks.x - 1, blecks.y)
                elif dir == 'w':
                    destination = (blecks.x, blecks.y - 1)
                elif dir == 's':
                    destination = (blecks.x, blecks.y + 1)
                else:
                    print('invalid command\n')
                    self.item_actions(item)

                if destination in npc_locations.values():
                    for key, value in npc_locations.items():
                        if value == destination:
                            npc_instance = key

                    self.inventory.remove(str(item))
                    npc_receive_item(str(npc_instance), str(item))
                elif destination in walls:
                    print('impossible!\n')
                    self.item_actions(item)
                else:
                    existing_items.append((str(item), destination))
                    self.inventory.remove(str(item))
                    normal_actions(f"you place the {item}")


        elif player_choice == 'x':
            self.inventory_actions()
        else:
            print('invalid command\n')
            self.item_actions(item)

    def inventory_actions(self):
        i = 1
        for x in self.inventory:
            print(str(i) + '. ' + x)
            i += 1
        player_choice = input('x = back\n')
        if player_choice.isnumeric() == True:
            chosen_item = self.inventory[int(player_choice) - 1]
            self.item_actions(chosen_item)
        elif player_choice == 'x':
            normal_actions()
        else:
            print('invalid command\n')
            self.inventory_actions()

def npc_receive_item(name, item):
        if name == 'tamel':
            if (str(item)) == 'dildo':
                normal_actions(f"{name}: oh I been needin one of those ;)")
            else:
                normal_actions(f"useless")
        else:
            normal_actions(f"{name}: a {item}, wow. thanks for it")

class Item:
    instances = []

    def __init__(self, x, y, name):
        self.name = str(name)
        self.x = x
        self.y = y
        self.base_damage = 0
        self.in_possession = False
        existing_items.append((self.name, (self.x, self.y)))
        self.__class__.instances.append(self)

#class Weapon(Item):



    def beep(self):
        print('big time beeps: ' + self.name)

def print_toolbar():
    global time
    global day
    contents = f"Time: {time}; Day: {day}; HP: {blecks.hp}; Gold: {blecks.gold};"
    print(contents)

def normal_actions(message=''):
    draw_grid(g)
    print(str(message) + '\n')
    player_choice = input('?\n')

    if player_choice == '?':
        print('wasd = move; e = inv; q = pick up')

    elif player_choice == 'a':
        blecks.move(player_choice)

    elif player_choice == 'd':
        blecks.move(player_choice)

    elif player_choice == 'w':
        blecks.move(player_choice)

    elif player_choice == 's':
        blecks.move(player_choice)

    elif player_choice == 'e':
        blecks.inventory_actions()

    elif player_choice == 'q':
        i = 0
        for x in existing_items:
            if (blecks.x, blecks.y) == x[1]:
                grabbed_item = str(x[0])
                blecks.inventory.append(str(x[0]))
                i += 1
                existing_items.remove(x)
        if i > 0:
            normal_actions(f"{grabbed_item} grabbed")
        else:
            normal_actions('nothing to pick up here ')

    else:
        normal_actions('invalid command')


intro = "Welcome, Blecks. It's the big city now. see for yourself...\n one character per command: \n wasd = move; e = inv; q = pick up"


blecks = Person('blecks')
npc1 = Person('tamel', 2, 3)
npc2 = Person('jimben', 4, 3)
poopoo = Item(2, 1, 'poopoo')
peepee = Item(3, 1, 'peepee')
nana = Item(3, 1, 'nana')
build_wall((5, 1), 7, 'y')
build_wall((0, 0), 50, 'x')
build_wall((49, 0), 15, 'y')
build_wall((0, 0), 15, 'y')
build_wall((0, 14), 50, 'x')
normal_actions(intro)
