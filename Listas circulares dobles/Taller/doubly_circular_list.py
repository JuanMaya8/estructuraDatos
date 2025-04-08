# doubly_circular_list.py

class BaseNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class HourNode(BaseNode):
    def __init__(self, roman_hour):
        super().__init__(roman_hour)

class MinuteNode(BaseNode):
    def __init__(self, minute_value):
        super().__init__(minute_value)

class DoublyCircularList:
    def __init__(self):
        self.head = None

    def append(self, value, node_type=BaseNode):
        new_node = node_type(value)

        if not self.head:
            self.head = new_node
            new_node.prev = new_node
            new_node.next = new_node
        else:
            tail = self.head.prev

            tail.next = new_node
            new_node.prev = tail

            new_node.next = self.head
            self.head.prev = new_node

    def find(self, value):
        if not self.head:
            return None

        current = self.head
        while True:
            if current.value == value:
                return current
            current = current.next
            if current == self.head:
                break
        return None

    def __iter__(self):
        current = self.head
        while True:
            yield current
            current = current.next
            if current == self.head:
                break
