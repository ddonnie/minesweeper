import sys
from Cell import *
from Group import *


def solve_mine(gamemap, result):

    def map_to_list(field):
        field = field[1:]
        another_map = []
        line = []
        for element in field:
            if element == "\n":
                another_map.append(line)
                line = []
                continue
            if element != ' ':
                if element.isdigit():
                    line.append(int(element))
                else:
                    line.append(element)
        return another_map

    def check_boundary(x, y):
        return (-1 < x < len(cellmap)) and (-1 < y < len(cellmap[row]))

    def open(row, column):
        if result[row][column] == 'x':
            print(row, column)
            sys.exit('KABOOM!')
        return result[row][column]

    gamemap = map_to_list(gamemap)
    result = map_to_list(result)
    cellmap = list(gamemap)

    print('initial map')
    print("\n".join(" ".join(map(str, row)) for row in cellmap))

    for row in range(len(cellmap)):
        for column in range(len(cellmap[row])):
            cellmap[row][column] = Cell(cellmap[row][column], (row, column))

    # print('*********************************************************')

    for row in range(len(cellmap)):
        for column in range(len(cellmap[row])):
            if cellmap[row][column].weight == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        x = row + i
                        y = column + j
                        if check_boundary(x, y):
                            cellmap[x][y].weight = open(x, y)
                            cellmap[x][y].is_open = True

    # print('*********************************************************')

    smth_changed = True

    while smth_changed:
        smth_changed = False
        groups = []
        for row in range(len(cellmap)):
            for column in range(len(cellmap[row])):
                if cellmap[row][column].is_open:
                    group = Group()
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            x = row + i
                            y = column + j
                            if check_boundary(x, y) and (cellmap[x][y].weight == '?' or cellmap[x][y].weight == 'x'):
                                group.cells.add(cellmap[x][y])
                                group.weight = cellmap[row][column].weight
                    if len(group.cells) > 0:
                        groups.append(group)

        repeat = True
        # print("********************begin of func********************")
        while repeat:
            repeat = False
            for current_group in groups:
                for compare_group in groups:
                    if current_group != compare_group:
                        if current_group.cells == compare_group.cells and current_group.weight == compare_group.weight:
                            # print("deleting", compare_group)
                            groups.remove(compare_group)
                            continue
                        if current_group.cells <= compare_group.cells:
                            compare_group.cells -= current_group.cells
                            compare_group.weight -= current_group.weight
                            repeat = True
                            continue
                        elif current_group.cells >= compare_group.cells:
                            current_group.cells -= compare_group.cells
                            current_group.weight -= compare_group.weight
                            repeat = True
                            continue
                        else:
                            if not current_group.cells.isdisjoint(compare_group.cells):
                                # print("MEETING", current_group, 'and', compare_group)
                                if current_group.weight > compare_group.weight:
                                    bigger = current_group
                                    smaller = compare_group
                                    # print('bigger is', bigger)
                                else:
                                    bigger = compare_group
                                    smaller = current_group
                                    # print('bigger is', bigger)
                                group = Group()
                                group.cells = current_group.cells.intersection(compare_group.cells)
                                # print ('New group cells is', group.cells)
                                group.weight = bigger.weight - (len(bigger.cells) - len(group.cells))
                                # print('New group weight is', group.weight)
                                if group.weight == smaller.weight:
                                    groups.append(group)
                                    bigger.cells -= group.cells
                                    bigger.weight -= group.weight
                                    smaller.cells -= group.cells
                                    smaller.weight -= group.weight
                                    # print('saving', bigger, smaller, group)
                                    repeat = True
        # print("***********************end of func************************")
        for group in groups:
            if group.weight == len(group.cells):
                for cell in group.cells:
                    row = cell.pos[0]
                    column = cell.pos[1]
                    cellmap[row][column].is_mine = True
                    cellmap[row][column].weight = 'x'
            if group.weight == 0:
                for cell in group.cells:
                    row = cell.pos[0]
                    column = cell.pos[1]
                    cellmap[row][column].weight = open(row, column)
                    cellmap[row][column].is_open = True
                    smth_changed = True

        # print('*********************************************************')
        #
        # for row in cellmap:
        #     print(row)
        # print('*********************************************************')

    for row in range(len(cellmap)):
        for column in range(len(cellmap[row])):
            if cellmap[row][column].weight == '?':
                print("solved")
                return("?")
    print("solved")
    return "\n".join(" ".join(map(str, row)) for row in cellmap)
