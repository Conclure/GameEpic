import random
import enum
import colorama as color
import replit


def random_bool():
    return True if random.randint(0, 1) == 1 else False


class MonsterAction(enum.Enum):
    ATTACK = 1
    DODGE = 2


class Direction(enum.Enum):
    NORTH = 1
    WEST = 2
    EAST = 3
    SOUTH = 4


class MonsterType(enum.Enum):
    BIG = "()"
    SMALL = "{}"
    MEDIUM = "<>"

    def __init__(self, symbol):
        self.symbol = symbol

    def pick_random():
        rand_i = random.randint(1, 3)
        if rand_i == 1:
            return MonsterType.BIG
        if rand_i == 2:
            return MonsterType.MEDIUM
        else:
            return MonsterType.SMALL


class Cell():
    def __init__(self, symbol):
        self.symbol = symbol
        self.pos = None
        self.world = None
        pass

    def reveal(self, cell):
        pass

    def __str__(self):
        result = {
            "pos": f"{self.pos}",
            "symbol": self.symbol
        }
        return f"{result}"


class EnemyCell(Cell):
    def __init__(self):
        super(EnemyCell, self).__init__("▓▓")
        self.monster = MonsterType.pick_random()

    def reveal(self, cell):
        self.symbol = self.monster.symbol
        options = {
            1: MonsterAction.ATTACK,
            2: MonsterAction.DODGE
        }

        while True:
            self.world.render()
            print(f"You encountered a monster! How do you respond?")

            for (i, action) in options.items():
                print(f"{i}. {action.name.capitalize()}")

            try:
                option_in = int(input(""))
            except:
                continue

            option = options.get(option_in)

            if option != None:
                break

        while True:
            self.world.render()
            if option == MonsterAction.DODGE:
                if random_bool():
                    print(f"You dodged! What do you do next?")
                elif random_bool():
                    print(f"The monster did not attack! What do you do next?")
                elif random_bool():
                    print(f"You tried dodging but failed, however the monster did not attack! What do you do next?")
                else:
                    print(f"You failed dodging and the monster killed you!")
                    break
            elif option == MonsterAction.ATTACK:
                if random_bool():
                    print(
                        f"You damaged the monster, however the monster flinched and could not move! What do you do next?")
                elif random_bool():
                    print(f"You damaged the monster and it damaged you back! What do you do next?")
                elif random_bool():
                    print(f"You killed the monster! What do you do next?")
                elif random_bool():
                    print(f"Your attack failed and the monster damaged you back! What do you do next?")
                elif random_bool():
                    print(f"Your attack failed and the monster attacked you back and killed you!")
                    break
                else:
                    print(f"You damaged the monster and it attacked you back and killed you!")
                    break

            for (i, action) in options.items():
                print(f"{i}. {action.name.capitalize()}")

            try:
                option_in = int(input(""))
            except:
                continue

            option = options.get(option_in)

            if option != None:
                continue


class EmptyCell(Cell):
    def __init__(self):
        super(EmptyCell, self).__init__("  ")


class HeroCell(Cell):
    def __init__(self):
        super(HeroCell, self).__init__(f"{color.Fore.RED}[]{color.Style.RESET_ALL}")


class GoalCell(Cell):
    def __init__(self):
        super(GoalCell, self).__init__("✨")


class Pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        result = {
            "x": self.x,
            "y": self.y
        }

        return f"{result}"


class World():
    def __init__(self, size):
        if size < 3:
            raise RuntimeError("Size must be greater than 3")
        self.arena = list()
        self.size = size
        for _ in range(size):
            row = list()
            for _ in range(size):
                row.append(None)
            self.arena.append(row)
        self.__generate()

    def __generate(self):
        for x in self.new_range():
            for y in self.new_range():
                pos = Pos(x, y)
                if random_bool() and random_bool() and random_bool():
                    self.populate(pos, EmptyCell())
                elif random_bool() and random_bool():
                    self.populate(pos, Cell("░░"))
                elif random_bool() and random_bool():
                    self.populate(pos, Cell("▒▒"))
                else:
                    self.populate(pos, EnemyCell())

    def populate(self, pos, cell):
        if pos.x > self.size or pos.x < 1:
            raise RuntimeError("X must not be greater than Size and not lower than 1")

        if pos.y > self.size or pos.y < 1:
            raise RuntimeError("Y must not be greater than Size and not lower than 1")

        self.arena[pos.y - 1][pos.x - 1] = cell
        cell.pos = pos
        cell.world = self

    def render(self):
        replit.clear()
        for row in self.arena:
            for cell in row:
                if cell == None:
                    print(" ", end="")
                else:
                    print(cell.symbol, end="")
            print("\n", end="")

    def new_range(self):
        return range(1, self.size + 1)

    def random_border_coordinate(self):
        if random_bool():
            y = random.randint(1, self.size)
            x = 1 if random_bool() else self.size
            return Pos(x, y)

        else:
            x = random.randint(1, self.size)
            y = 1 if random_bool() else self.size
            return Pos(x, y)

    def opposite_coordinate(self, pos):
        if pos.x > self.size or pos.x < 1:
            raise RuntimeError("X must not be greater than Size and not lower than 1")

        if pos.y > self.size or pos.y < 1:
            raise RuntimeError("Y must not be greater than Size and not lower than 1")
        x = self.size - pos.x + 1
        y = self.size - pos.y + 1
        return Pos(x, y)

    def get_possible_directions(self, cell):
        result = [
            Direction.NORTH,
            Direction.WEST,
            Direction.EAST,
            Direction.SOUTH
        ]
        cord = cell.pos
        if cord.x == 1:
            result.remove(Direction.WEST)
        if cord.x == self.size:
            result.remove(Direction.EAST)
        if cord.y == 1:
            result.remove(Direction.NORTH)
        if cord.y == self.size:
            result.remove(Direction.SOUTH)
        return result

    def get_cell(self, pos):
        return self.arena[pos.y - 1][pos.x - 1]

    # TODO
    def get_cell_offset(self, pos, direction):
        if direction == Direction.NORTH:
            return self.arena[pos.y - 2][pos.x - 1]
        elif direction == Direction.SOUTH:
            return self.arena[pos.y][pos.x - 1]
        elif direction == Direction.WEST:
            return self.arena[pos.y - 1][pos.x - 2]
        elif direction == Direction.EAST:
            return self.arena[pos.y - 1][pos.x]


def main():
    size = 20
    world = World(size)

    hero = HeroCell()
    goal = GoalCell()
    world.populate(world.random_border_coordinate(), hero)
    world.populate(world.opposite_coordinate(hero.pos), goal)

    directions = world.get_possible_directions(hero)
    options = {}
    for (i, direction) in enumerate(directions):
        options[i + 1] = direction
    option = None
    while True:
        world.render()
        print(f"Where do you want to walk?")

        for (i, direction) in options.items():
            print(f"{i}. {direction.name.capitalize()}")

        try:
            option_in = int(input(""))
        except:
            continue

        option = options.get(option_in)

        if option != None:
            break

    offset = world.get_cell_offset(hero.pos, option)
    offset.reveal(hero)


if __name__ == "__main__":
    main()
