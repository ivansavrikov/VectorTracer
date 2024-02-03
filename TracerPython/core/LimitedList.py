from collections import deque

class LimitedList:
    def __init__(self, max_length):
        self.items = deque(maxlen=max_length)

    def add(self, item):
        self.items.append(item)

    def get(self, index):
        return self.items[index]

    def get_all(self):
        return list(self.items)

# my_list = LimitedList(max_length=2)

# my_list.add(1)
# my_list.add(2)

# print(f'\n{my_list.get_all()}\n')
# my_list.add(3)
# print(f'\n{my_list.get_all()}\n')
# print(f'\n{my_list.get(0)}, {my_list.get(1)}\n')
