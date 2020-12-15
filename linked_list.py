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

    def get_item(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("linked list index out of range")
        node = self._get_to_index(index)
        self.cached_node = node
        self.cached_index = index
        return node.item

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

    def _get_to_index(self, target_idx):
        start_idx = 0
        step = 1
        node = self.head
        if self.cached_index != -1:
            delta = target_idx - self.cached_index
            if abs(delta) < target_idx:
                # it is faster to start from the cached index
                start_idx = self.cached_index
                step = 1 if delta >= 0 else -1
                node = self.cached_node
        idx_steps = str(node.item)
        for i in range(start_idx, target_idx, step):
            node = node.next if (step == 1) else node.prev
            idx_steps = idx_steps + " " + str(node.item)
        #print("get to index steps:", idx_steps)
        return node

    # item_added: True if item was just added, False if remove
    # item_index: which item was just added or subtracted
    def _adjust_cache(self, item_added, item_index):
        if self.cached_index == -1: return
        if item_added:
            if item_index <= self.cached_index:
                self.cached_index = self.cached_index + 1
        else:
            # item removed
            if self.length == 0:
                self.cached_index = -1
                self.cached_node = None
            else:
                if item_index == self.cached_index:
                    # We deleted the cached node
                    self.cached_node = None
                    self.cached_index = -1
                elif item_index < self.cached_index:
                    self.cached_index = self.cached_index - 1
        if self.cached_index >= self.length:
            self.cached_index = self.length - 1

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



