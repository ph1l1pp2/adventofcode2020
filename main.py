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
    pass


def day6_2():
    pass


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
