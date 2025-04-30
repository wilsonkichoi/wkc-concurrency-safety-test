import random


def inflate_and_shuffle(data: list, size: int) -> list:
    length = len(data)
    new_data = []
    if length < size:
        quotient, remainder = divmod(size, length)
        new_data.extend(data * quotient)
        new_data.extend(random.choices(data, k=remainder))
    elif length > size:
        new_data = random.choices(data, k=size)
    else:
        new_data = data[:]
    
    random.shuffle(new_data)

    return new_data
