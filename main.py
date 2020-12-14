import copy
import re
from typing import List, Dict, Set, Tuple


def day1_1():
    expenses = []
    with open("input.txt", "r") as f:
        for line in f:
            expenses.append(int(line))
    expenses_2020 = get_two_with_sum(values=expenses, target_sum=2020)
    return expenses_2020[0] * expenses_2020[1]


def day1_2():
    expenses = []
    with open("input.txt", "r") as f:
        for line in f:
            expenses.append(int(line))
    for x in expenses:
        expenses_2020 = get_two_with_sum(values=expenses, target_sum=2020 - x)
        if expenses_2020:
            return expenses_2020[0] * expenses_2020[1] * x


def get_two_with_sum(values: List[int], target_sum: int):
    return [x for x in values if target_sum - x in values]


def day2_1():
    valid_passwords = []
    with open("input_pw.txt", "r") as f:
        for line in f:
            parts = line.split()
            times = parts[0].split("-")
            letter = parts[1][0]
            password = parts[2]
            if int(times[0]) <= password.count(letter) <= int(times[1]):
                valid_passwords.append(line)
    return len(valid_passwords)


def day2_2():
    valid_passwords = []
    with open("input_pw.txt", "r") as f:
        for line in f:
            parts = line.split()
            positions = parts[0].split("-")
            letter = parts[1][0]
            password = parts[2]
            position_1 = letter == password[int(positions[0]) - 1]
            position_2 = letter == password[int(positions[1]) - 1]
            if position_1 or position_2:
                if not (position_1 and position_2):
                    valid_passwords.append(line)
    return len(valid_passwords)


def day3_1():
    with open("input_3.txt", "r") as f:
        grid = f.readlines()
    return count_trees(grid=grid, right=3, down=1)


def count_trees(grid: List[str], right: int, down: int):
    x = 0
    trees = 0
    for i, y in enumerate(grid):
        if i % down == 0:
            if y[x % (len(y) - 1)] == "#":
                trees += 1
            x += right
    return trees


def day3_2():
    with open("input_3.txt", "r") as f:
        grid = f.readlines()
    trees = count_trees(grid=grid, right=1, down=1)
    trees = trees * count_trees(grid=grid, right=3, down=1)
    trees = trees * count_trees(grid=grid, right=5, down=1)
    trees = trees * count_trees(grid=grid, right=7, down=1)
    trees = trees * count_trees(grid=grid, right=1, down=2)
    return trees


def day4_1():
    passports = read_passports()
    valid = [p for p in passports if not get_missing_required_fields(p)]
    return len(valid)


def read_passports() -> List[Dict[str, str]]:
    passports = []
    passport = []
    with open("input_4.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                passport = passport + line.split()
            else:
                passports.append(passport)
                passport = []
        passports.append(passport)
    return [{f.split(":")[0]: f.split(":")[1] for f in p} for p in passports]


def get_missing_required_fields(passport: Dict[str, str]) -> List[str]:
    required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    return [rf for rf in required_fields if rf not in passport.keys()]


def day4_2():
    passports = read_passports()
    passports = [p for p in passports if not get_missing_required_fields(p)]
    passports = [p for p in passports if is_passport_valid(p)]
    return len(passports)


def is_passport_valid(passport: Dict[str, str]) -> bool:
    for k, v in passport.items():
        if not is_passport_field_valid(k, v):
            return False
    return True


def is_passport_field_valid(k: str, v: str) -> bool:
    if k in ["byr", "iyr", "eyr"]:
        if not v.isnumeric() or len(v) != 4:
            return False
        elif k == "byr" and 1920 <= int(v) <= 2002:
            return True
        elif k == "iyr" and 2010 <= int(v) <= 2020:
            return True
        elif k == "eyr" and 2020 <= int(v) <= 2030:
            return True
        else:
            return False
    if k == "hgt":
        if v[-2:] == "cm" and 150 <= int(v[:-2]) <= 193:
            return True
        elif v[-2:] == "in" and 59 <= int(v[:-2]) <= 76:
            return True
        else:
            return False
    if k == "hcl":
        if re.search(r"^#[0-9a-f]{6}$", v):
            return True
        else:
            return False
    if k == "ecl":
        if v in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return True
        else:
            return False
    if k == "pid":
        if v.isnumeric() and len(v) == 9:
            return True
        else:
            return False
    if k == "cid":
        return True


def day5_1():
    return max([get_seat_id(s) for s in get_seats()])


def get_seats():
    with open("input_5.txt", "r") as f:
        seats = []
        for line in f:
            row = line[0:7]
            row = row.replace("F", "0")
            row = row.replace("B", "1")
            column = line[7:]
            column = column.replace("L", "0")
            column = column.replace("R", "1")
            seats.append((int(row, 2), int(column, 2)))
    return seats


def get_seat_id(seat: Tuple[int, int]) -> int:
    row, column = seat
    return row * 8 + column


def day5_2():
    seat_ids = [get_seat_id(s) for s in get_seats()]
    free_seats = [s for s in range(max(seat_ids)) if s not in seat_ids]
    return [s for s in free_seats if s + 1 in seat_ids and s - 1 in seat_ids]


def day6_1():
    groups_answers_yes = []
    for group in get_groups():
        answer_yes = set()
        for person in group:
            for answer in person:
                answer_yes.add(answer)
        groups_answers_yes.append(answer_yes)
    return sum([len(a) for a in groups_answers_yes])


def get_groups():
    groups = []
    group = []
    with open("input_6.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line != "":
                group.append(line)
            else:
                groups.append(group)
                group = []
        groups.append(group)
    return groups


def day6_2():
    groups_answers_yes = []
    for group in get_groups():
        group_answer_yes = set()
        for i, person in enumerate(group):
            person_answer_yes = set()
            for answer in person:
                person_answer_yes.add(answer)
            if i == 0:
                group_answer_yes = person_answer_yes
            else:
                group_answer_yes = group_answer_yes.intersection(person_answer_yes)
        groups_answers_yes.append(group_answer_yes)
    return sum([len(a) for a in groups_answers_yes])


def day7_1():
    rules = read_rules()
    bag_color = "shiny gold"
    bags = can_be_contained_by(bag_color, rules)
    return len(bags)


def can_be_contained_by(bag_color: str, rules: Dict) -> Set:
    colors = {k for k, v in rules.items() if bag_color in v.keys()}
    if colors:
        for color in colors:
            colors = colors.union(can_be_contained_by(bag_color=color, rules=rules))
    return colors


def read_rules():
    rules = {}
    with open("input_7.txt", "r") as f:
        for line in f:
            outer_bag, inner_bags = line.split("contain")
            outer_bag_parts = outer_bag.split()
            outer_bag_color = f"{outer_bag_parts[0]} {outer_bag_parts[1]}"
            inner_bags_parsed = {}
            if inner_bags.strip() != "no other bags.":
                inner_bags = inner_bags.split(",")
                for inner_bag in inner_bags:
                    inner_bag_parts = inner_bag.split()
                    inner_bag_count = int(inner_bag_parts[0])
                    inner_bag_color = f"{inner_bag_parts[1]} {inner_bag_parts[2]}"
                    inner_bags_parsed[inner_bag_color] = inner_bag_count
            rules[outer_bag_color] = inner_bags_parsed
    return rules


def day7_2():
    rules = read_rules()
    bag_color = "shiny gold"
    bags = count_containing(bag_color=bag_color, rules=rules)
    return bags


def count_containing(bag_color: str, rules: Dict) -> int:
    count = 0
    bags_contained = rules.get(bag_color, None)
    if bags_contained:
        for color, c in bags_contained.items():
            count += c
            count += c * count_containing(bag_color=color, rules=rules)
    return count


def day8_1():
    boot_code = get_boot_code()
    accumulator, boot_error = execute_boot_code(boot_code=boot_code)
    return accumulator


def day8_2():
    boot_code = get_boot_code()
    swap_instruction = {"jmp": "nop", "nop": "jmp"}
    for i, line in enumerate(boot_code):
        operation, argument = line
        if operation != "acc":
            fixed_boot_code = boot_code.copy()
            fixed_boot_code[i] = (swap_instruction[operation], argument)
            accumulator, boot_error = execute_boot_code(boot_code=fixed_boot_code)
            if not boot_error:
                return accumulator


def get_boot_code() -> List[Tuple[str, int]]:
    boot_code = []
    with open("input_8.txt", "r") as f:
        for line in f:
            operation, argument = line.split()
            boot_code.append((operation, int(argument)))
    return boot_code


def execute_boot_code(boot_code: List[Tuple[str, int]]):
    i = 0
    accumulator = 0
    already_run = []
    while i < len(boot_code) and i not in already_run[:-1]:
        operation, argument = boot_code[i]
        if operation == "acc":
            accumulator += argument
            i += 1
        elif operation == "jmp":
            i += argument
        elif operation == "nop":
            i += 1
        already_run.append(i)
    error = True if i < len(boot_code) else False
    return accumulator, error


def day9_1():
    with open("input_9.txt", "r") as f:
        data = [int(line.strip()) for line in f.readlines()]
    preamble = 25
    while data[preamble] in get_sums(data[:preamble]):
        data.pop(0)
    return data[preamble]


def get_sums(values: List[int]) -> List[int]:
    return [x + y for y in values for x in values if x != y]


def day9_2():
    with open("input_9.txt", "r") as f:
        data = [int(line.strip()) for line in f.readlines()]
    weakness = day9_1()
    for i in range(len(data)):
        for j in range(2, len(data)):
            if sum(data[i:j]) == weakness:
                return min(data[i:j]) + max(data[i:j])
            elif sum(data[i:j]) > weakness:
                continue


def day10_1():
    with open("input_10.txt", "r") as f:
        data = [int(line.strip()) for line in f.readlines()]
    builtin_adapter_voltage = max(data) + 3
    data.append(0)
    data.append(builtin_adapter_voltage)
    data.sort()
    voltage_differences = [j - i for i, j in zip(data[:-1], data[1:])]
    voltage_differences_count = [voltage_differences.count(i + 1) for i in range(3)]
    return voltage_differences_count[0] * voltage_differences_count[2]


def day11_1():
    with open("input_11.txt", "r") as f:
        ferry_seats = [[seat for seat in line.strip()] for line in f.readlines()]
    new_ferry_seats = apply_seating_rules(seats=ferry_seats)
    while ferry_seats != new_ferry_seats:
        ferry_seats = new_ferry_seats
        new_ferry_seats = apply_seating_rules(seats=ferry_seats)
    return sum([len([seat for seat in row if seat == "#"]) for row in new_ferry_seats])


def apply_seating_rules(seats: List[List[str]]) -> List[List[str]]:
    new_seats = copy.deepcopy(seats)
    for seat_row, row in enumerate(seats):
        for seat_column, column in enumerate(row):
            adjacent_seats = count_adjacent_seats(row=seat_row, column=seat_column, seats=seats)
            if column == "L" and adjacent_seats["#"] == 0:
                new_seats[seat_row][seat_column] = "#"
            elif column == "#" and adjacent_seats["#"] >= 4:
                new_seats[seat_row][seat_column] = "L"
    return new_seats


def count_adjacent_seats(row: int, column: int, seats: List[List[str]]) -> Dict[str, int]:
    adjacent_seats = {"#": 0, "L": 0, ".": 0}
    for check_row in range((row - 1 if row > 0 else row), (row + 1 if row + 1 < len(seats) else row) + 1):
        for check_columns in range((column - 1 if column > 0 else column),
                                   (column + 1 if column + 1 < len(seats[0]) else column) + 1):
            if check_row != row or check_columns != column:
                adjacent_seats[seats[check_row][check_columns]] += 1
    return adjacent_seats


def day12_1():
    with open("input_12.txt", "r") as f:
        instructions = [(line[0], int(line[1:].strip())) for line in f.readlines()]
    ship = Ship()
    for instruction in instructions:
        ship.perform_instruction(instruction=instruction)
    return abs(ship.pos_x) + abs(ship.pos_y)


class Ship:
    directions = {"N": 0, "E": 90, "S": 180, "W": 270}

    def __init__(self, start_pos=(0, 0), start_heading=90, start_waypoint=(0, 0)):
        self.pos_x, self.pos_y = start_pos
        self.waypoint_x, self.waypoint_y = start_waypoint
        self.heading = start_heading

    def perform_instruction(self, instruction):
        action, value = instruction
        if action in self.directions.keys():
            self.move(direction=self.directions[action], value=value)
        elif action == "F":
            self.move(direction=self.heading, value=value)
        elif action in ["L", "R"]:
            self.turn(degree=value, action=action)

    def move(self, direction: int, value: int):
        if direction == 0:
            self.pos_y += value
        elif direction == 90:
            self.pos_x += value
        elif direction == 180:
            self.pos_y -= value
        elif direction == 270:
            self.pos_x -= value

    def turn(self, degree: int, action: str):
        if action == "R":
            self.heading = (self.heading + degree) % 360
        elif action == "L":
            self.heading = (self.heading - degree) % 360

    def perform_waypoint_instruction(self, instruction):
        action, value = instruction
        if action in self.directions.keys():
            self.move_waypoint(direction=self.directions[action], value=value)
        elif action == "F":
            self.move_waypoint_direction(value=value)
        elif action in ["L", "R"]:
            self.rotate_waypoint(degree=value, action=action)

    def move_waypoint(self, direction: int, value: int):
        if direction == 0:
            self.waypoint_y += value
        elif direction == 90:
            self.waypoint_x += value
        elif direction == 180:
            self.waypoint_y -= value
        elif direction == 270:
            self.waypoint_x -= value

    def move_waypoint_direction(self, value: int):
        self.pos_x += value * self.waypoint_x
        self.pos_y += value * self.waypoint_y

    def rotate_waypoint(self, degree: int, action: str):
        if degree == 180:
            self.waypoint_x *= (-1)
            self.waypoint_y *= (-1)
        elif (degree == 90 and action == "L") or (degree == 270 and action == "R"):
            self.waypoint_x, self.waypoint_y = self.waypoint_y * (-1), self.waypoint_x
        elif (degree == 90 and action == "R") or (degree == 270 and action == "L"):
            self.waypoint_x, self.waypoint_y = self.waypoint_y, self.waypoint_x * (-1)


def day12_2():
    with open("input_12.txt", "r") as f:
        waypoint_instructions = [(line[0], int(line[1:].strip())) for line in f.readlines()]
    ship = Ship(start_waypoint=(10, 1))
    for waypoint_instruction in waypoint_instructions:
        ship.perform_waypoint_instruction(instruction=waypoint_instruction)
    return abs(ship.pos_x) + abs(ship.pos_y)


def day13_1():
    earliest_time = 1006605
    bus_lines = "19,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,883,x,x,x,x,x,x,x,23,x,x,x,x,13,x,x,x,17,x,x,x,x,x,x,x,x,x,x" \
                ",x,x,x,797,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,29".split(",")
    bus_lines = [int(i) for i in bus_lines if i != "x"]
    wait_time, bus = get_next_bus(earliest_time=earliest_time, bus_lines=bus_lines)
    return wait_time * bus[0]


def get_next_bus(earliest_time: int, bus_lines: List[int]) -> Tuple[int, List[int]]:
    for wait_time in range(min(bus_lines)):
        bus = [bus_line for bus_line in bus_lines if (earliest_time + wait_time) % bus_line == 0]
        if bus:
            return wait_time, bus


def day13_2():
    # should be optimized by using some math tricks
    bus_lines = "19,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,883,x,x,x,x,x,x,x,23,x,x,x,x,13,x,x,x,17,x,x,x,x,x,x,x,x,x,x" \
                ",x,x,x,797,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,29".split(",")
    bus_lines = [int(i) if i != "x" else None for i in bus_lines]
    leave_time = 100000000000000

    max_bus_line = max([i for i in bus_lines if i])
    max_bus_line_diff_first = bus_lines.index(max_bus_line)
    leave_time = leave_time - (leave_time % max_bus_line) - max_bus_line_diff_first
    while True:
        if check_buses(leave_time=leave_time, bus_lines=bus_lines):
            return leave_time
        leave_time += max_bus_line


def check_buses(leave_time: int, bus_lines: List[int]):
    return all([((leave_time + i) % bus) == 0 for i, bus in enumerate(bus_lines) if bus])


def day14_1():
    instructions = []
    with open("input_14.txt", "r") as f:
        for line in f:
            instruction, value = line.split("=")
            instructions.append((instruction.strip(), value.strip()))
    mask = ""
    memory = {}
    for instruction, value in instructions:

        if instruction == "mask":
            mask = value
            print(mask)
        else:
            address = instruction[instruction.find("[")+1:instruction.find("]")]
            value_str = bin(int(value))[2:].zfill(36)
            memory[address] = "".join([x for x in map(apply_bit_mask, mask, value_str)])
    return sum([int(m, 2) for m in memory.values()])


def apply_bit_mask(mask_bit, value_bit):
    if mask_bit == "X":
        return value_bit
    else:
        return mask_bit




if __name__ == '__main__':
    print(day1_1())
    print(day1_2())
    print(day2_1())
    print(day2_2())
    print(day3_1())
    print(day3_2())
    print(day4_1())
    print(day4_2())
    print(day5_1())
    print(day5_2())
    print(day6_1())
    print(day6_2())
    print(day7_1())
    print(day7_2())
    print(day8_1())
    print(day8_2())
    print(day9_1())
    # print(day9_2())
    # print(day10_1())

    # print(day11_1())

    print(day12_1())
    print(day12_2())
    print(day13_1())
    # print(day13_2())
    print(day14_1())
