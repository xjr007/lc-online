def binary_search(binary_sequence, item):
    front_number = 0
    last_number = len(binary_sequence) - 1
    while front_number <= last_number:
        middle_number = (front_number + last_number) // 2
        if item == binary_sequence[middle_number]:
            return binary_sequence[middle_number]
        elif item < binary_sequence[middle_number]:
            last_number = middle_number - 1
        elif item > binary_sequence[middle_number]:
            front_number = middle_number + 1
    return "Not found"
