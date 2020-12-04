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
        expenses_2020 = get_two_with_sum(values=expenses, target_sum=2020-x)
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


if __name__ == '__main__':
    # print(day1_1())
    # print(day1_2())
    print(day2_1())

