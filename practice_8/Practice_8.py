def replace_first_20(numbers):
    if 20 in numbers:
        index = numbers.index(20)
        numbers[index] = 200
    return numbers


def remove_empty_strings(strings):
    return list(filter(None, strings))

def square_numbers(numbers):
    return [num ** 2 for num in numbers]


def remove_all_20(numbers):
    return [num for num in numbers if num != 20]


def main():
    numbers1 = [5, 10, 15, 20, 25, 20, 30]
    print(numbers1)
    print(replace_first_20(numbers1))

    strings = ["hello", "", "world", "", "python", ""]
    print(strings)
    print(remove_empty_strings(strings))

    numbers3 = [1, 2, 3, 4, 5]
    print(numbers3)
    print(square_numbers(numbers3))

    numbers4 = [10, 20, 30, 20, 40, 20, 50]
    print(numbers4)
    print(remove_all_20(numbers4))


if __name__ == "__main__":
    main()
