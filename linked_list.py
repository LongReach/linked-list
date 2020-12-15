# Implementation of a linked list. It is doubly-linked. There is a caching feature, for keeping track of last
# node accessed. That way, if we try to get an item at a particular index, we might be able to get to it
# more quickly.

class ListNode(object):

    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class LinkedList(object):

    class NodeRef:
        def __init__(self, node=None, index=-1):
            self.node = node
            self.index = index

        def clear(self):
            self.node = None
            self.index = -1


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

    # Empties the list
    def clear(self):
        self.head = None
        self.tail = None
        self.length = 0
        self.cached_node = None
        self.cached_index = -1

    # Reverses the list in place
    def reverse_list(self):
        node = self.head
        while node:
            orig_next = node.next
            node.next = node.prev
            node.prev = orig_next
            node = orig_next
        orig_tail = self.tail
        self.tail = self.head
        self.head = orig_tail
        if self.cached_index != -1:
            self.cached_index = self.length - 1 - self.cached_index

    # Adds item to head of linked list
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

    # Adds item to tail of linked list
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

    # Inserts item into list, before item at specified index. If index == length of list, place after last item.
    def insert(self, item, index=0):
        if index < 0 or index > self.length:
            raise IndexError("linked list index out of range")
        if index == 0:
            self.add_head(item)
        elif index == self.length:
            self.add_tail(item)
        else:
            node_to_precede = self._get_to_index(index)
            new_node = ListNode(item)
            new_node.prev = node_to_precede.prev
            new_node.next = node_to_precede
            if new_node.prev is not None:
                new_node.prev.next = new_node
            node_to_precede.prev = new_node
            self.length = self.length + 1
            self.cached_node = new_node
            self.cached_index = index

    # Pops item from head of list, returns item
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

    # Pops item from tail of list, returns item
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

    # Returns current size of list
    def size(self):
        return self.length

    # Gets item at index. Tries to use caching for extra speed.
    def get_item(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("linked list index out of range")
        node = self._get_to_index(index)
        self.cached_node = node
        self.cached_index = index
        return node.item

    # Locates item in list, starting from start_index.
    # Params
    #   item: item to find
    #   start_index: if given, index to start searching from. -1 is the same as not giving an index.
    #   backwards: if true, we search backwards
    # Returns index of item
    def find_item(self, item, start_index=None, backwards=False):
        if start_index is None or start_index == -1:
            start_index = self.length-1 if backwards else 0
        if start_index < 0 or start_index >= self.length:
            raise IndexError("linked list index out of range")
        node = self._get_to_index(start_index)
        idx = start_index
        while node is not None:
            if node.item == item:
                self.cached_node = node
                self.cached_index = idx
                return idx
            idx = idx + (-1 if backwards else 1)
            node = node.prev if backwards else node.next
        raise ValueError("Item not found in linked list")

    # Returns a Python list of items in list
    def get_items(self):
        ret_list = []
        node = self.head
        while(node):
            ret_list.append(node.item)
            node = node.next
        return ret_list

    # For debugging purposes, changes the cached node
    def _new_cache_item(self, idx):
        if self.length == 0: return
        node = self.head
        for i in range(idx):
            node = node.next
        self.cached_node = node
        self.cached_index = idx

    # Returns node at target_idx, takes advantage of caching
    def _get_to_index(self, target_idx):
        # The idea is to pick the closest starting point: head of list, tail, or cached node
        # Each tuple: a delta value, a starting index, node
        options = [(target_idx, 0, self.head), # representing start of linked list
                         (target_idx - (self.length-1), self.length-1, self.tail)] # end of l. list

        if self.cached_index != -1:
            # There is a cached node
            options.append((target_idx - self.cached_index, self.cached_index, self.cached_node))

        # Find best option
        best_delta = self.length
        best_op = options[0]
        for tup in options:
            if abs(tup[0]) < best_delta:
                best_delta = abs(tup[0])
                best_op = tup

        node = best_op[2]
        step = -1 if best_op[0] < 0 else 1 # delta to target
        for i in range(best_op[1], target_idx, step):
            node = node.next if (step == 1) else node.prev

        return node

    # If an item is added to or removed from linked list, we need to change index of cached node
    # item_added: True if item was just added, False if removed
    # item_index: which item was just added or subtracted
    def _adjust_cache(self, item_added, item_index):
        if self.cached_index == -1:
            # We don't have a cached node, so pick one and exit
            if self.length > 0:
                target_idx = int(self.length / 2) # go to middle of list
                self.cached_node = self._get_to_index(target_idx)
                self.cached_index = target_idx
            return

        if item_added:
            if item_index <= self.cached_index:
                self.cached_index = self.cached_index + 1 # cached node index pushed to right
        else:
            # item removed
            if self.length == 0:
                # The list is now empty
                self.cached_index = -1
                self.cached_node = None
            else:
                if item_index == self.cached_index:
                    # Cached node pointer was pointing to node that got deleted
                    self.cached_node = None
                    self.cached_index = -1
                elif item_index < self.cached_index:
                    self.cached_index = self.cached_index - 1
        if self.cached_index >= self.length:
            self.cached_index = self.length - 1

    # Debugging feature; tests the linked list for validity. Returns False if list invalid, error code string
    def _validate(self):
        error_str = ""
        count, node = 0, self.head
        while node:
            node = node.next
            count = count + 1
        if count != self.length:
            error_str = "bad length, forward"
            return False, error_str
        count, node = 0, self.tail
        while node:
            node = node.prev
            count = count + 1
        if count != self.length:
            error_str = "bad length, backward"
            return False, error_str
        if self.head is None and self.tail is not None:
            error_str = "only tail defined"
            return False, error_str
        if self.head is not None and self.tail is None:
            error_str = "only head defined"
            return False, error_str
        if self.cached_index == -1:
            if self.cached_node is not None:
                error_str = "cached node doesn't match index"
                return False, error_str
        else:
            node = self.head
            for i in range(self.cached_index):
                node = node.next
            if node is not self.cached_node:
                error_str = "cached node doesn't match index"
                return False, error_str
        return True, ""



