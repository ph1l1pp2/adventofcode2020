
def day1_1():
    expenses = []
    with open("input.txt", "r") as f:
        for line in f:
            expenses.append(int(line))
    expenses_2020 = [x for x in expenses if 2020 - x in expenses]
    return expenses_2020[0]*expenses_2020[1]


if __name__ == '__main__':
    print(day1_1())


