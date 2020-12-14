class ListNode(object):

    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class LinkedList(object):

    def __init__(self, iterable):

        self.head = None
        self.tail = None
        self.length = 0

        if iterable is not None:
            for i in iterable:
                self.add_tail(i)

    def add_head(self, item):

        node = ListNode(item)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.length = self.length + 1

    def add_tail(self, item):

        node = ListNode(item)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.length = self.length + 1

    def pop_head(self):

        if self.head is None: return None
        ret_node = self.head
        self.head = ret_node.next
        if self.head is not None:
            self.head.prev = None
        if self.tail is ret_node:
            self.tail = None
        self.length = self.length - 1
        return ret_node.item

    def pop_tail(self):

        if self.tail is None: return None
        ret_node = self.tail
        self.tail = ret_node.prev
        if self.tail is not None:
            self.tail.next = None
        if self.head is ret_node:
            self.head = None
        self.length = self.length - 1
        return ret_node.item

    def size(self):
        return self.length

    def get_items(self):
        ret_list = []
        node = self.head
        while(node):
            ret_list.append(node.item)
            node = node.next
        return ret_list

words = ["alpha", "bravo", "charlie", "delto", "echo", "foxtrot"]

ll = LinkedList(words)
print("list is:", ll.get_items())
print("length is:", ll.size())
ll.pop_head()
print("popped head, list is:", ll.get_items())
print("length is:", ll.size())
ll.pop_tail()
print("popped tail, list is:", ll.get_items())
print("length is:", ll.size())
ll.add_head("A")
print("new head, list is:", ll.get_items())
print("length is:", ll.size())
ll.add_tail("F")
print("new tail, list is:", ll.get_items())
print("length is:", ll.size())

