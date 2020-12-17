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
            self.idx = index

        def set(self, node, index):
            self.node = node
            self.idx = index

        def clear(self):
            self.node = None
            self.idx = -1

        def valid(self):
            return self.node is not None

        def empty(self):
            return self.node is None

        def increment(self):
            if self.node is not None:
                self.idx = self.idx + 1

        def decrement(self):
            if self.node is not None:
                self.idx = self.idx - 1

        def assign(self, other_ref):
            self.node = other_ref.node
            self.idx = other_ref.idx

        def copy(self):
            return LinkedList.NodeRef(self.node, self.idx)


    def __init__(self, iterable=None):
        self.head_ref = LinkedList.NodeRef()
        self.tail_ref = LinkedList.NodeRef()
        # if we deal with a node that's not the head or tail, cached_node/cached_index keep track of it
        self.cached_ref = LinkedList.NodeRef()

        if iterable is not None:
            for i in iterable:
                self.add_tail(i)

    # --------------------------------------
    # Functions for broadly changing list
    # --------------------------------------

    # Empties the list
    def clear(self):
        self.head_ref.clear()
        self.tail_ref.clear()
        self.cached_ref.clear()

    # Reverses the list in place
    def reverse_list(self):
        size = self.size()
        if size == 0: return
        node = self.head_ref.node
        while node:
            orig_next = node.next
            node.next = node.prev
            node.prev = orig_next
            node = orig_next
        orig_tail = self.tail_ref.node
        self.tail_ref.set(self.head_ref.node, size-1)
        self.head_ref.set(orig_tail, 0)
        if self.cached_ref.idx != -1:
            self.cached_ref.idx = size - 1 - self.cached_ref.idx

    # --------------------------------------
    # Functions for adding items
    # --------------------------------------

    # Adds item to head of linked list
    def add_head(self, item):
        node = ListNode(item)
        if self.size() == 0:
            self.head_ref.set(node, 0)
            self.tail_ref.set(node, 0)
        else:
            node.next = self.head_ref.node
            self.head_ref.node.prev = node
            self.head_ref.set(node, 0)
            self.tail_ref.increment()
        self._adjust_cache(True, 0)

    # Adds item to tail of linked list
    def add_tail(self, item):
        node = ListNode(item)
        size = self.size()
        if size == 0:
            self.head_ref.set(node, 0)
            self.tail_ref.set(node, 0)
        else:
            node.prev = self.tail_ref.node
            self.tail_ref.node.next = node
            self.tail_ref.set(node, size)
        self._adjust_cache(True, size)

    # Inserts item into list, before item at specified index. If index == length of list, place after last item.
    def insert(self, item, index=0):
        if index < 0 or index > self.size():
            raise IndexError("linked list index out of range")
        if index == 0:
            self.add_head(item)
        elif index == self.size():
            self.add_tail(item)
        else:
            node_to_precede = self._get_to_index(index)
            new_node = ListNode(item)
            new_node.prev = node_to_precede.prev
            new_node.next = node_to_precede
            if new_node.prev is not None:
                new_node.prev.next = new_node
            node_to_precede.prev = new_node
            self.tail_ref.increment()
            self.cached_ref.set(new_node, index)

    # --------------------------------------
    # Functions for removing items
    # --------------------------------------

    # Pops item from head of list, returns item
    def pop_head(self):
        if self.size() == 0: return
        ret_node = self.head_ref.node
        self.head_ref.set(ret_node.next, 0)
        if self.head_ref.valid():
            self.head_ref.node.prev = None
        if self.tail_ref.node is ret_node:
            self.tail_ref.clear()
        self.tail_ref.decrement()
        self._adjust_cache(False, 0)
        return ret_node.item

    # Pops item from tail of list, returns item
    def pop_tail(self):
        size = self.size()
        if size == 0: return
        ret_node = self.tail_ref.node
        self.tail_ref.set(ret_node.prev, size-2)
        if self.tail_ref.valid():
            self.tail_ref.node.next = None
        if self.head_ref.node is ret_node:
            self.head_ref.clear()
        self._adjust_cache(False, size - 1)
        return ret_node.item

    def remove(self, index=0):
        if index < 0 or (index > 0 and index >= self.size()):
            print("bad index is",index,"size is", self.size())
            raise IndexError("linked list index {} out of range".format(index))
        if index == 0:
            return self.pop_head()
        elif index == self.size()-1:
            return self.pop_tail()
        else:
            node_to_remove = self._get_to_index(index)
            if node_to_remove.prev is not None:
                node_to_remove.prev.next = node_to_remove.next
            if node_to_remove.next is not None:
                node_to_remove.next.prev = node_to_remove.prev
            self.tail_ref.decrement()
            self._adjust_cache(False, index)
            return node_to_remove.item

    # --------------------------------------
    # Functions for getting items or information
    # --------------------------------------

    # Returns current size of list
    def size(self):
        if self.head_ref.empty() or self.tail_ref.empty(): return 0
        return self.tail_ref.idx - self.head_ref.idx + 1

    def empty(self):
        return self.size() == 0

    # Gets item at index. Tries to use caching for extra speed.
    def get_item(self, index):
        if index < 0 or index >= self.size():
            raise IndexError("linked list index out of range")
        node = self._get_to_index(index)
        self.cached_ref.set(node, index)
        return node.item

    # Locates item in list, starting from start_index.
    # Params
    #   item: item to find
    #   start_index: if given, index to start searching from. -1 is the same as not giving an index.
    #   backwards: if true, we search backwards
    # Returns index of item
    def find_item(self, item, start_index=None, backwards=False):
        if start_index is None or start_index == -1:
            start_index = self.size()-1 if backwards else 0
        if start_index < 0 or start_index >= self.size():
            raise IndexError("linked list index out of range")
        node = self._get_to_index(start_index)
        idx = start_index
        while node is not None:
            if node.item == item:
                self.cached_ref.set(node, idx)
                return idx
            idx = idx + (-1 if backwards else 1)
            node = node.prev if backwards else node.next
        raise ValueError("Item not found in linked list")

    # Returns a Python list of items in list
    def get_items(self):
        ret_list = []
        node = self.head_ref.node
        while(node):
            ret_list.append(node.item)
            node = node.next
        return ret_list

    # For debugging purposes, changes the cached node
    def _new_cache_item(self, idx):
        if self.size() == 0: return
        node = self.head_ref.node
        for i in range(idx):
            node = node.next
        self.cached_ref.set(node, idx)

    # Returns node at target_idx, takes advantage of caching
    def _get_to_index(self, target_idx):
        # The idea is to pick the closest starting point: head of list, tail, or cached node
        # Each tuple: a delta value, a starting index, node
        options = [(target_idx, 0, self.head_ref.node), # representing start of linked list
                         (target_idx - (self.size()-1), self.size()-1, self.tail_ref.node)] # end of l. list

        if self.cached_ref.valid():
            # There is a cached node
            options.append((target_idx - self.cached_ref.idx, self.cached_ref.idx, self.cached_ref.node))

        # Find best option
        best_delta = self.size()
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
        if self.cached_ref.idx == -1:
            # We don't have a cached node, so pick one and exit
            if self.size() > 0:
                target_idx = int(self.size() / 2) # go to middle of list
                self.cached_ref.set(self._get_to_index(target_idx), target_idx)
            return

        if item_added:
            if item_index <= self.cached_ref.idx:
                self.cached_ref.increment() # cached node index pushed to right
        else:
            # item removed
            if self.size() == 0:
                # The list is now empty
                self.cached_ref.clear()
            else:
                if item_index == self.cached_ref.idx:
                    # Cached node pointer was pointing to node that got deleted
                    self.cached_ref.clear()
                elif item_index < self.cached_ref.idx:
                    self.cached_ref.decrement()
        if self.cached_ref.idx >= self.size():
            self.cached_ref.decrement()

    # Debugging feature; tests the linked list for validity. Returns False if list invalid, error code string
    def _validate(self):
        error_str = ""
        count, node = 0, self.head_ref.node
        while node:
            node = node.next
            count = count + 1
        if count != self.size():
            error_str = "bad length, forward"
            return False, error_str
        count, node = 0, self.tail_ref.node
        while node:
            node = node.prev
            count = count + 1
        if count != self.size():
            error_str = "bad length, backward"
            return False, error_str
        if self.head_ref.empty() and self.tail_ref.valid():
            error_str = "only tail defined"
            return False, error_str
        if self.head_ref.valid() and self.tail_ref.empty():
            error_str = "only head defined"
            return False, error_str
        if self.cached_ref.idx == -1:
            if self.cached_ref.node is not None:
                error_str = "cached node doesn't match index"
                return False, error_str
        else:
            node = self.head_ref.node
            for i in range(self.cached_ref.idx):
                node = node.next
            if node is not self.cached_ref.node:
                error_str = "cached node doesn't match index"
                return False, error_str
        return True, ""



