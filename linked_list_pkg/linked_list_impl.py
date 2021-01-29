# Implementation of a linked list. It is doubly-linked. There is a caching feature, for keeping track of last
# node accessed. That way, if we try to get an item at a particular index, we might be able to get to it
# more quickly.

class ListNode(object):

    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class LinkedList(object):

    # Helper class. Refers to a node in a linked list with both the node pointer and its index in the list.
    # For now, its two main purposes are for implementing the cached node and for implementing the Python
    # iterator. I might later make this class more useful to outside callers.
    class NodeRef:
        def __init__(self, node=None, index=-1):
            self.node = node
            self.idx = index

        # For iterator support
        def __next__(self):
            node = self.node
            if node is None:
                raise StopIteration
            self.node = self.node.next
            self.idx = self.idx + 1
            return node.item

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

    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self.length = 0
        self._rebuild_cache()

        if iterable is not None:
            for i in iterable:
                node = ListNode(i)
                self._add_to_tail_internal(node)
            self._rebuild_cache()

    # Support for iteration using 'for'. A NodeRef object serves as the iterator.
    def __iter__(self):
        return LinkedList.NodeRef(self.head, 0)

    def __sizeof__(self):
        return self.length

    # --------------------------------------
    # Functions for adding items
    # --------------------------------------

    # Adds item to head of linked list
    def add_head(self, item):
        node = ListNode(item)
        if self.size() == 0:
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
        old_size = self.length
        node = ListNode(item)
        self._add_to_tail_internal(node)
        self._adjust_cache(True, old_size)

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
            self.length = self.length + 1
            self._adjust_cache(True, index)

    # A helper function that doesn't do cache adjustments
    def _add_to_tail_internal(self, node):
        if self.length == 0:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.length = self.length + 1

    # --------------------------------------
    # Functions for removing items
    # --------------------------------------

    # Pops item from head of list, returns item
    def pop_head(self):
        if self.size() == 0: return
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
        size = self.size()
        if size == 0: return
        ret_node = self.tail
        self.tail = ret_node.prev
        if self.tail is not None:
            self.tail.next = None
        if self.head is ret_node:
            self.head = None
        self.length = self.length - 1
        self._adjust_cache(False, size - 1)
        return ret_node.item

    # Removes item at specified index, returns item
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
            self.length = self.length - 1
            self._adjust_cache(False, index)
            return node_to_remove.item

    # --------------------------------------
    # Functions for getting items or information
    # --------------------------------------

    # Returns current size of list
    def size(self):
        return self.length

    def empty(self):
        return self.size() == 0

    # Gets item at index. Tries to use caching for extra speed.
    def get_item(self, index):
        if index < 0 or index >= self.size():
            raise IndexError("linked list index out of range")
        node = self._get_to_index(index)
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

    # --------------------------------------
    # Functions for broadly changing list
    # --------------------------------------

    # Empties the list
    def clear(self):
        self.head = None
        self.tail = None
        self.length = 0
        self.cached_nodes = []
        self.num_valid_cache_entries = 0

    # Makes a copy of this list
    def copy(self):
        new_list = LinkedList()
        node = self.head
        while node:
            new_list.add_tail(node.item)
            node = node.next
        return new_list

    # Reverses the list in place
    def reverse_list(self):
        size = self.size()
        if size == 0: return
        node = self.head
        while node:
            orig_next = node.next
            node.next = node.prev
            node.prev = orig_next
            node = orig_next
        orig_tail = self.tail
        self.tail = self.head
        self.head = orig_tail
        # TODO: revisit this
        self._rebuild_cache()

    # Sorts the list. If the val_func is set, it must return a particular piece of data from the object stored in
    # the list (presumably, they're all of the same type). Otherwise, the objects themselves will be compared.
    def sort(self, reverse=False, val_func=None):
        _compare_func = self._get_compare_func(val_func, reverse)
        size = self.size()
        if size == 0 or size == 1: return
        new_start_node = self._merge_sort_sublist(self.head, self.tail, 0, size-1, _compare_func)
        self.head = new_start_node
        new_tail_node = new_start_node
        while new_tail_node.next is not None:
            new_tail_node = new_tail_node.next
        self.tail = new_tail_node
        self._rebuild_cache()

    # Given another linked list, join its contents to the tail of this one. The other list is cleared.
    def join(self, other_list):
        size = self.size()
        size2 = other_list.size()
        if size == 0:
            self.head = other_list.head
            self.tail = other_list.tail
        else:
            tail_node = self.tail
            tail_node.next = other_list.head
            if tail_node.next is not None:
                tail_node.next.prev = tail_node
            new_tail_node = other_list.tail
            if new_tail_node is None:
                new_tail_node = tail_node
            self.tail = new_tail_node
        self.length = size + size2
        other_list.clear()
        self._rebuild_cache()

    # Splits off a separate linked list, beginning with the item at index. If index is the same as the size of
    # the list, then return an empty linked list.
    def split(self, index):
        size = self.size()
        if index < 0 or index > size:
            raise IndexError("linked list index out of range")
        new_list = LinkedList()
        if index == size:
            # simply return an empty list
            return new_list
        split_node = self._get_to_index(index)
        new_tail = split_node.prev
        if new_tail is not None:
            new_tail.next = None
        new_list.head = split_node
        new_list.tail = self.tail
        new_list.length = size - index
        self.tail = new_tail
        self.length = index
        self._rebuild_cache()
        return new_list

    # --------------------------------------
    # Private helper functions, for internal use
    # --------------------------------------

    # Rebuilds the cache by stepping through the list, periodically recording a cache node
    def _rebuild_cache(self):
        self.cached_nodes = []
        self.num_valid_cache_entries = 0
        cache_size = 10 if self.length <= 10 else (50 if self.length <= 1000 else 100);
        skip_amount = 1 if cache_size >= self.length else int(self.length / cache_size)
        self.cached_nodes = [LinkedList.NodeRef() for i in range(cache_size)]
        cache_idx = 0
        list_idx = 0
        node = self.head
        while node is not None and cache_idx < cache_size:
            self.cached_nodes[cache_idx].set(node, list_idx)
            for n in range(skip_amount):
                node = node.next
                if node is None: break
            list_idx = list_idx + skip_amount
            cache_idx = cache_idx + 1
        self.num_valid_cache_entries = cache_idx
        self.list_length_at_cache_rebuild = self.length

    def _cache_needs_rebuild(self):
        # Has list shrunk or grown significantly since last cache rebuild?
        if self.list_length_at_cache_rebuild < int(self.length * 0.66):
            return True
        elif self.list_length_at_cache_rebuild > int(self.length * 1.33):
            return True
        # Have a lot of cache entries been invalidated?
        if self.num_valid_cache_entries < int(len(self.cached_nodes) * 0.66):
            return True
        return False

    # Returns node at target_idx, takes advantage of caching to get there more quickly
    def _get_to_index(self, target_idx):
        # The idea is to pick the closest starting point: head of list, tail, or cached node
        # Each tuple: a delta value, a starting index, node
        options = [(target_idx, 0, self.head), # representing start of linked list
                         (target_idx - (self.size()-1), self.size()-1, self.tail)] # end of l. list

        for n in range(len(self.cached_nodes)):
            if self.cached_nodes[n].valid():
                # There is a cached node
                options.append((target_idx - self.cached_nodes[n].idx, self.cached_nodes[n].idx, self.cached_nodes[n].node))

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
        if self._cache_needs_rebuild():
            self._rebuild_cache()
            return

        if item_added:
            # If item inserted at n, all cache entries of index n or greater are shifted right
            for n in range(len(self.cached_nodes)):
                if self.cached_nodes[n].idx >= item_index:
                    self.cached_nodes[n].idx = self.cached_nodes[n].idx + 1
        else:
            # If item removed at n, all cache entries of index n+1 or greater are shifted left. Index n is cleared.
            for n in range(len(self.cached_nodes)):
                if self.cached_nodes[n].idx == item_index:
                    self.cached_nodes[n].clear()
                    self.num_valid_cache_entries = self.num_valid_cache_entries - 1
                elif self.cached_nodes[n].idx > item_index:
                    self.cached_nodes[n].idx = self.cached_nodes[n].idx - 1

    # The val_func, if specified, returns the value for comparison. If reverse is True, we are going higher-to-lower
    # instead of lower to higher.
    def _get_compare_func(self, val_func, reverse):
        def _val_func(item):
            return item
        if not val_func: val_func = _val_func

        def _compare_func(n1, n2): # Returns True if n1, n2 in correct order
            return not reverse if val_func(n1.item) < val_func(n2.item) else reverse
        return _compare_func

    # Given a sublist, use merge sort to sort it. Returns new start node of sorted sublist. The compare function
    # returns true of the first item should come first.
    def _merge_sort_sublist(self, start_node, end_node, start_index, end_index, compare_func):
        if start_index >= end_index:
            start_node.next = None
            return start_node
        if (end_index - start_index) == 1:
            # swap the nodes, if necessary
            if not compare_func(start_node, end_node): # Returns True if first node should come first
                end_node.next = start_node # end node becomes start node
                start_node.prev = end_node # start node becomes end node
                end_node.prev = None
                start_node.next = None
                return end_node

        median_node = start_node
        median_index = int((start_index + end_index) / 2)
        for i in range(0, median_index-start_index):
            median_node = median_node.next
        median_plus_one_node = median_node.next
        #print("median node is", median_node.item)
        new_start_node = self._merge_sort_sublist(start_node, median_node, start_index, median_index, compare_func)
        new_median_node = self._merge_sort_sublist(median_plus_one_node, end_node, median_index+1, end_index, compare_func)
        result = self._merge_lists(new_start_node, new_median_node, compare_func)
        return result

    # Given two lists that have already been sorted using the same compare_func, merge them together
    def _merge_lists(self, list1_start, list2_start, compare_func):
        # TODO: could be a little more efficient
        new_head = None
        tail = None
        node1 = list1_start
        node2 = list2_start
        while node1 is not None and node2 is not None:
            choice = None
            if compare_func(node1, node2): # Returns True if first node should come first
                choice = node1
                node1.prev = None
                node1 = node1.next
            else:
                choice = node2
                node2.prev = None
                node2 = node2.next
            if new_head is None:
                new_head = choice
            choice.prev = tail
            if tail is not None:
                tail.next = choice
            tail = choice # the next pointer will continue to point where it was
        if node1 is not None:
            tail.next = node1
            node1.prev = tail
        elif node2 is not None:
            tail.next = node2
            node2.prev = tail
        return new_head




