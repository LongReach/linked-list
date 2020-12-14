
class ListNode(object):

    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class LinkedList(object):

    def __init__(self, iterable=None):

        self.head = None
        self.tail = None
        self.length = 0
        # if we deal with a node that's not the head or tail, cached_node/cached_index keep track of it
        self.cached_node = None
        self.cached_index = -1

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
        self._adjust_cache(True, 0)

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
        self._adjust_cache(True, self.length-1)

    def pop_head(self):

        if self.head is None: return None
        ret_node = self.head
        self.head = ret_node.next
        if self.head is not None:
            self.head.prev = None
        if self.tail is ret_node:
            self.tail = None
        self.length = self.length - 1
        self._adjust_cache(False, 0)
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
        self._adjust_cache(False, self.length)
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

    def _new_cache_item(self, idx):
        if self.length == 0: return
        node = self.head
        for i in range(idx):
            node = node.next
        self.cached_node = node
        self.cached_index = idx

    def _adjust_cache(self, item_added, item_index):
        if self.cached_index == -1: return
        if item_added:
            if item_index < self.cached_index:
                self.cached_index = self.cached_index + 1
        else:
            # item removed
            if self.length == 0:
                self.cached_index = -1
                self.cached_node = None
            else:
                if item_index < self.cached_index:
                    self.cached_index = self.cached_index - 1
        if self.cached_index >= self.length:
            self.cached_index = self.length - 1



def print_list_details(the_list, operation=None):
    if operation is not None:
        print("operation:", operation)
    print("list is:", the_list.get_items())
    print("    length is:", the_list.size())
    print("    cached index:", the_list.cached_index)
    print("    cached item:", "NONE" if the_list.cached_node is None else the_list.cached_node.item)
    print("--------------------")

words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]
ll = LinkedList(words)
ll._new_cache_item(3)
print_list_details(ll)
ll.pop_head()
print_list_details(ll, "popped head")
ll.pop_tail()
print_list_details(ll, "popped tail")
ll.add_head("A")
print_list_details(ll, "added head")
ll.add_tail("F")
print_list_details(ll, "added tail")

ll2 = LinkedList()
ll2.add_head("two")
ll2.add_head("one")
ll2._new_cache_item(0)
print_list_details(ll2)
ll2.pop_head()
print_list_details(ll2, "pop head")
ll2.pop_head()
print_list_details(ll2, "pop head")
ll2.add_head("---")
print_list_details(ll2, "add head")
