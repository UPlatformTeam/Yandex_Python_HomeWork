import sys
import random
from random import randint
import matplotlib.pyplot as plt
# from enum import Enum
# python3 is used

class Cell(object):

    FISH = 1
    SHARK = 2
    EMPTY = 3
    DIRTY = 4

    def get_type(self):
        return self.type


class Empty(Cell):

    def __init__(self):
        self.type = Cell.EMPTY

    def __str__(self):
        return '0'


class Dirty(Cell):

    def __init__(self):
        self.type = Cell.DIRTY

    def __str__(self):
        return '1'


class Animal(Cell):
    def __init__(self):
        self.division_counter = 0
        self.alive = True
        self.ready_for_partition = False

    def increase_division_counter(self):
        self.division_counter += 1
        if self.division_counter > self.division_period:
            self.ready_for_partition = True
            self.division_counter = 0

    def choose_direction(self, buff_grid, i, j):
        pass


class Shark(Animal):

    def __init__(self):
        super(Shark, self).__init__()
        self.type = Cell.SHARK
        self.life_durability = randint(5, 7)
        self.life_counter = 0
        self.division_period = 2 * self.life_durability + 2

    def __str__(self):
        return 'S'

    def increase_life_counter(self):
        self.life_counter += 1
        if self.life_counter > self.life_durability:
            self.alive = False

    def choose_direction(self, ocean, buff_grid, i, j):

            posses = []  # possible directions to move
            posses_fishes = []  # possible directions to eat a fish
            arr = [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]

            for direction in arr:
                new_i, new_j = direction

                if (
                    not ocean.is_bound(new_i, new_j) and
                    not is_shark(buff_grid[new_i][new_j]) and
                    not is_dirty(buff_grid[new_i][new_j])
                ):
                    posses.append([new_i, new_j])

                if (
                    not ocean.is_bound(new_i, new_j) and
                    is_fish(ocean.grid[new_i][new_j])
                ):
                    posses_fishes.append([new_i, new_j])

            if len(posses) == 0:
                # buff_grid[i][j] = self.grid[i][j]
                return i, j
            else:
                if len(posses_fishes) != 0:
                    new_i, new_j = choose_neighbour(posses_fishes)
                    return new_i, new_j
                else:
                    new_i, new_j = choose_neighbour(posses)
                    return new_i, new_j


class Fish(Animal):
    def __init__(self):
        super(Fish, self).__init__()
        self.type = Cell.FISH
        self.division_period = randint(2, 5)

    def __str__(self):
        return 'F'

    def choose_direction(self, ocean, buff_grid, i, j):

            posses = []  # possible directions to move
            arr = [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]

            for direction in arr:
                new_i, new_j = direction
                if (
                        not ocean.is_bound(new_i, new_j) and
                        is_empty(buff_grid[new_i][new_j])
                ):
                    posses.append([new_i, new_j])

            if len(posses) == 0:
                return i, j
            else:
                new_i, new_j = choose_neighbour(posses)
                return new_i, new_j


def is_shark(cell):
    return cell.get_type() == Cell.SHARK


def is_fish(cell):
    return cell.get_type() == Cell.FISH


def is_dirty(cell):
    return cell.get_type() == Cell.DIRTY


def is_empty(cell):
    return cell.get_type() == Cell.EMPTY


def choose_neighbour(posses):
    random_value = randint(0, len(posses) - 1)
    new_i, new_j = posses[random_value]
    return new_i, new_j


class Ocean:

    def __init__(self, W, H):
        self.W = W + 1
        self.H = H + 1
        self.grid = [[Empty() for i in range(self.H + 1)]
                     for i in range(self.W + 1)]
        self.shark_prob = 0.02
        self.fish_prob = 0.06

    def fill_species(self):

        for i in range(1, self.W):
            for j in range(1, self.H):
                prob = random.uniform(0.0, 1.0)
                if prob < self.shark_prob:
                    self.grid[i][j] = Shark()
                elif prob < self.shark_prob + self.fish_prob:
                    self.grid[i][j] = Fish()

    def is_bound(self, x, y):
        return x == 0 or y == 0 or x == self.W or y == self.H

    def __str__(self):
        string = '[\n'
        for i in range(1, self.W):
            for j in range(1, self.H):
                string += str(self.grid[i][j])
            string += '\n'
        string += ']'
        return string

    def clear_sharks(self):
        # this part of code deletes those sharks,
        # who died and increases life_counter for sharks

        for i in range(1, self.W):
            for j in range(1, self.H):
                if not is_shark(self.grid[i][j]):
                    continue
                self.grid[i][j].increase_life_counter()
                if not self.grid[i][j].alive:
                    self.grid[i][j] = Empty()

    def move_objects(self):
        # this part of code moves all objects

        buff_grid = [[Empty() for i in range(self.H + 1)]
                     for i in range(self.W + 1)]

        for i in range(self.W):
            for j in range(self.H):
                if is_fish(self.grid[i][j]):
                    buff_grid[i][j] = self.grid[i][j]
                if is_shark(self.grid[i][j]):
                    buff_grid[i][j] = self.grid[i][j]

        for i in range(1, self.W):
            for j in range(1, self.H):
                if not is_shark(self.grid[i][j]) and not is_fish(self.grid[i][j]):
                    continue

                new_i, new_j = self.grid[i][j].choose_direction(self, buff_grid, i, j)

                # if is_shark(self.grid[i][j]):
                #     new_i, new_j = self.choose_direction_shark(buff_grid, i, j)
                # else:
                #     new_i, new_j = self.choose_direction_fish(buff_grid, i, j)

                if is_shark(self.grid[i][j]):
                    if is_fish(self.grid[new_i][new_j]):
                        self.grid[i][j].life_counter = 0
                        self.grid[new_i][new_j] = Empty()
                    buff_grid[new_i][new_j] = self.grid[i][j]
                    if new_i != i or new_j != j:
                        buff_grid[i][j] = Empty()
                else:
                    buff_grid[new_i][new_j] = self.grid[i][j]
                    if new_i != i or new_j != j:
                        buff_grid[i][j] = Empty()

        self.grid = buff_grid

    def division(self):
        # this part of code makes all creatures to divide

        for i in range(1, self.W):
            for j in range(1, self.H):
                if is_empty(self.grid[i][j]):
                    continue

                self.grid[i][j].increase_division_counter()

                if self.grid[i][j].ready_for_partition:
                    not self.grid[i][j].ready_for_partition
                    posses = []
                    arr = [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]

                    for direction in arr:
                        new_i = direction[0]
                        new_j = direction[1]
                        if (
                            not self.is_bound(new_i, new_j) and
                            is_empty(self.grid[new_i][new_j])
                        ):
                            posses.append([new_i, new_j])

                    if len(posses) == 0:
                        continue
                    else:
                        new_i, new_j = choose_neighbour(posses)
                        if is_shark(self.grid[i][j]):
                            self.grid[new_i][new_j] = Shark()
                        else:
                            self.grid[new_i][new_j] = Fish()

    def calc_creatures_on_field(self):
        # this part of code calculates all sharks and fishes
        sharks = 0
        fishs = 0
        for i in range(1, self.H):
            for j in range(1, self.W):

                if str(self.grid[i][j]) == 'S':
                    sharks += 1

                if str(self.grid[i][j]) == 'F':
                    fishs += 1
        return sharks, fishs

    def iteration(self):
        self.clear_sharks()
        # self.move_fishes()
        # self.move_sharks()
        self.move_objects()
        self.division()
        sharks, fishs = self.calc_creatures_on_field()
        return sharks, fishs

    def iterate(self, num, console=False):
        li = []

        for it in range(0, num):
            if it % 100 == 0:
                print (it)
            sharks, fishs = self.iteration()
            li.append([sharks, fishs])

            if console:
                print ('sharks=', sharks)
                print ('fishs=', fishs)
                print (self)
        return li


def main():

    ocean = Ocean(20, 20)
    ocean.fill_species()
    print (str(ocean))

    li = ocean.iterate(1000, console=False)

    x = []
    y = []
    z = []

    for i in range(len(li)):
        x.append(i)
        y.append(li[i][0])
        z.append(li[i][1])

    plt.figure(figsize=(50, 10))
    plt.scatter(x, y, c='blue', alpha=0.75, cmap='winter')
    plt.scatter(x, z, c='red', alpha=0.75, cmap='winter')
    plt.xlim(0, max(x))
    plt.ylim(0, (ocean.W - 1) * (ocean.H - 1))
    plt.show()

if __name__ == '__main__':
    main()
