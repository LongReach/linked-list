from linked_list_pkg import LinkedList

validity_failure = False

# This decorator is important for testing. It wraps most of the functions in the LinkedList class, allowing an
# examination of the list after each change to it. If the verbosity level is high, some information is printed
# out after each operation on the list. If the verbosity level is low, the wrapper function only prints messages about
# errors with the list.
def test_function_decorator(func_to_wrap):
    # ref is to the linked list
    def wrapper(ref, *argc, **kwargs):
        global validity_failure
        result = func_to_wrap(ref, *argc, **kwargs)
        # is there an expected list?
        expected_list = kwargs.get('expected_list')
        valid, error_str = ref.validate() # Test the validity of the list
        if ref.last_operation_str is not None: # The name of the operation, e.g. "add_head", "pop_tail"
            if ref.verbosity >= TestList.MEDIUM:
                print("last_operation_str:", ref.last_operation_str)
        if ref.verbosity == TestList.HIGH:
            print("list is:", ref.get_items())
            print("    length is:", ref.size())
            print("    cached index:", ref.cached_ref.idx)
            print("    cached item:", "NONE" if ref.cached_ref.empty() else ref.cached_ref.node.item)
        if not valid:
            validity_failure = True
            print("    *** validity failed ***, error code:", error_str)
        if expected_list is not None: # compare to a Python list of expected items
            match = True
            the_items = ref.get_items()
            if len(expected_list) != len(the_items):
                match = False
            else:
                for i, item in enumerate(expected_list):
                    if expected_list[i] != the_items[i]:
                        match = False
            if not match:
                validity_failure = True
                print("    *** expected result failure ***:", expected_list)
        if ref.verbosity == TestList.HIGH:
            print("--------------------")
        return result
    return wrapper

# This subclass of LinkedList wraps many of its functions with the test function above
class TestList(LinkedList):

    LOW = 0
    MEDIUM = 1
    HIGH = 2

    def __init__(self, iterable=None):
        self.verbosity = TestList.LOW
        super().__init__(iterable)
        self.last_operation_str = "" # a string representation of the last operation, e.g. "add_tail"

    # The decorated functions wrap the same functions in base class. In each case, the expected_list parameter
    # can be a Python list that contains the expected items

    @test_function_decorator
    def reverse_list(self, expected_list=None):
        self.last_operation_str = "reverse_list"
        super().reverse_list()

    @test_function_decorator
    def add_head(self, item, expected_list=None):
        self.last_operation_str = "add_head, item={}".format(item)
        super().add_head(item)

    @test_function_decorator
    def add_tail(self, item, expected_list=None):
        self.last_operation_str = "add_tail, item={}".format(item)
        super().add_tail(item)

    @test_function_decorator
    def insert(self, item, index=0, expected_list=None):
        self.last_operation_str = "insert, item={} at {}".format(item, index)
        super().insert(item, index)

    @test_function_decorator
    def pop_head(self, expected_list=None):
        self.last_operation_str = "pop_head"
        return super().pop_head()

    @test_function_decorator
    def pop_tail(self, expected_list=None):
        self.last_operation_str = "pop_tail"
        return super().pop_tail()

    @test_function_decorator
    def remove(self, index=0, expected_list=None):
        self.last_operation_str = "remove, index={}".format(index)
        return super().remove(index)

    @test_function_decorator
    def get_item(self, index, expected_list=None):
        self.last_operation_str = "get_item, index={}".format(index)
        return super().get_item(index)

    @test_function_decorator
    def find_item(self, item, start_index=None, backwards=False, expected_list=None):
        self.last_operation_str = "find_item, item={} at {}, backwards={}".format(item, start_index, backwards)
        return super().find_item(item, start_index, backwards)

    @test_function_decorator
    def copy(self, expected_list=None):
        self.last_operation_str = "copy"
        result = super().copy()
        return TestList(result.get_items()) # A bit of a hack, but fine for testing

    @test_function_decorator
    def sort(self, reverse=False, val_func=None, expected_list=None):
        self.last_operation_str = "sort"
        return super().sort(reverse, val_func)

    @test_function_decorator
    def join(self, other_list, expected_list=None):
        self.last_operation_str = "join"
        super().join(other_list)

    @test_function_decorator
    def split(self, index, expected_list=None):
        self.last_operation_str = "split"
        result = super().split(index)
        return TestList(result.get_items()) # A bit of a hack, but fine for testing

    @test_function_decorator
    def test_new_cache_item(self, idx, expected_list=None):
        self.last_operation_str = "new_cached_item, idx={}".format(idx)
        self._new_cache_item(idx)

    def compare(self, expected_list):
        if self.length != len(expected_list):
            return False
        i = 0
        node = self.head
        while(node):
            if node.item != expected_list[i]: return False
            node = node.next
            i = i + 1
        return True

    # Debugging feature; tests the linked list for validity. Returns False if list invalid, error code string
    def validate(self):
        error_str = ""
        count, node = 0, self.head
        while node:
            node = node.next
            count = count + 1
        if count != self.size():
            error_str = "bad length, forward"
            return False, error_str
        count, node = 0, self.tail
        while node:
            node = node.prev
            count = count + 1
        if count != self.size():
            error_str = "bad length, backward"
            return False, error_str
        if self.head is None and self.tail is not None:
            error_str = "only tail defined"
            return False, error_str
        if self.head is not None and self.tail is None:
            error_str = "only head defined"
            return False, error_str
        if self.cached_ref.idx == -1:
            if self.cached_ref.node is not None:
                error_str = "cached node doesn't match index"
                return False, error_str
        else:
            node = self.head
            for i in range(self.cached_ref.idx):
                node = node.next
            if node is not self.cached_ref.node:
                error_str = "cached node doesn't match index"
                return False, error_str
        return True, ""
