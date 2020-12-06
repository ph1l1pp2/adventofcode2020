from typing import List


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


if __name__ == '__main__':
    print(day1_1())
    print(day1_2())
    print(day2_1())
    print(day2_2())
    print(day3_1())
    print(day3_2())
