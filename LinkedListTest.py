import random
import time
import argparse
from linked_list import LinkedList

parser = argparse.ArgumentParser(description='Tester program for LinkedListClass.')
parser.add_argument("--verbosity", help="Verbosity level (0=verbose, 1=semi-verbose, 2=silent)", type=int, default=1)
parser.add_argument("--seed", help="A seed for random number generation (to reproduce same tests)", type=int, default=-1)
args = parser.parse_args()

verbosity = args.verbosity
random_seed = args.seed
validity_failure = False
failed_tests = []

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

    # Debugging feature; tests the linked list for validity. Returns False if list invalid, error code string
    def validate(self):
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


if random_seed == -1:
    # choose a seed at random (sort of)
    random_seed = int(time.time()) % 100000
random.seed(random_seed)


# First test: a few simple operations on a predefined linked list

print("\nTEST ONE")
words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]
callsign_ll = TestList(words)
callsign_ll.verbosity = verbosity
callsign_ll.test_new_cache_item(3)
callsign_ll.reverse_list()
callsign_ll.reverse_list()
callsign_ll.pop_head()
callsign_ll.pop_tail(expected_list=['bravo', 'charlie', 'delta', 'echo'])
callsign_ll.add_head("A")
callsign_ll.add_tail("F")
if validity_failure:
    failed_tests.append("TEST ONE")
    validity_failure = False

# Second test: a few simple operations on another predefined linked list

print("\nTEST TWO")
number_ll = TestList()
number_ll.verbosity = verbosity
number_ll.add_head("two")
number_ll.add_head("one")
number_ll.test_new_cache_item(0)
number_ll.pop_head()
number_ll.pop_head(expected_list=[])
number_ll.add_head("zzz", expected_list=["zzz"])
if validity_failure:
    failed_tests.append("TEST TWO")
    validity_failure = False

# Third test: more list modifications. Also, we try searches for indices NOT in the list.

print("\nTEST THREE")
fruit_ll = TestList(["apple", "orange", "pear", "banana", "grape", "lemon", "lime", "grapefruit"])
fruit_ll.verbosity = verbosity
fruit_ll.get_item(2)
fruit_ll.get_item(5)
fruit_ll.get_item(3)
fruit_ll.insert("coconut", 3)
fruit_ll.insert("tomato", 0)
bad_indices = [17, -1, 500, -3]
for bi in bad_indices:
    try:
        fruit_ll.get_item(bi)
    except IndexError:
        print("index out of range, as expected")
    else:
        print("did not fail index-out-of-range test, as expected")
        validity_failure = True
if validity_failure:
    failed_tests.append("TEST THREE")
    validity_failure = False

# Fourth test: perform finds on same list as last test. Some finds are expected to succeed, others to fail

print("\nFIND TEST")
# We should have: ['tomato', 'apple', 'orange', 'pear', 'coconut', 'banana', 'grape', 'lemon', 'lime', 'grapefruit']
# Each tuple: item, start index, reverse or not
valid_finds = [("coconut", 0, False), ("apple", 4, True), ("lime", 3, False), ("pear", -1, True)]
fail_finds = [("apple", 4, False), ("sandwich", -1, False), ("kiwi", -1, True), ("lemon", 4, True), ("banana", 77, False)]
finds = [valid_finds, fail_finds]
for find_list in finds:
    for f in find_list:
        try:
            find_str = "found:" if find_list is valid_finds else "couldn't find:"
            print("{} {} starting from {}{}".format(find_str, f[0], f[1], ", reverse=True" if f[2] else ""))
            fruit_ll.find_item(f[0], f[1], f[2])
        except (ValueError, IndexError):
            if find_list is valid_finds:
                print("failed find for {} where success was expected".format(f[0]))
        else:
            if find_list is fail_finds:
                print("successful find for {} where failure was expected".format(f[0]))
if validity_failure:
    failed_tests.append("FIND TEST")
    validity_failure = False

# Fifth test:
# This test creates an empty list, then performs a series of random operations on it, putting in random numbers
# At the same time, we perform the same operations on a regular Python list, which we compare to the linked list.

print("\nRANDOM TEST: seed={}".format(random_seed))
rand_ll = TestList()
rand_ll.verbosity = verbosity
python_list = []
for i in range(20):
    random_num = random.randrange(10000)
    operations = ["add_head", "add_tail", "pop_head", "pop_tail", "insert", "remove"]
    rand_op = random.randrange(6)
    rand_index = 0
    if rand_op == 0:
        rand_ll.add_head(random_num)
        python_list.insert(0, random_num)
    elif rand_op == 1:
        rand_ll.add_tail(random_num)
        python_list.append(random_num)
    elif rand_op == 2:
        rand_ll.pop_head()
        if len(python_list) > 0:
            python_list.pop(0)
    elif rand_op == 3:
        rand_ll.pop_tail()
        if len(python_list) > 0:
            python_list.pop()
    elif rand_op == 4:
        rand_index = 0 if rand_ll.size() == 0 else random.randrange(rand_ll.size())
        rand_ll.insert(random_num, rand_index)
        python_list.insert(rand_index, random_num)
    elif rand_op == 5:
        rand_index = 0 if rand_ll.size() == 0 else random.randrange(rand_ll.size())
        rand_ll.remove(rand_index)
        if len(python_list) > 0:
            python_list.pop(rand_index)
    op_str = operations[rand_op]
    if rand_op == 0 or rand_op == 1 or rand_op == 4 or rand_op == 5:
        op_str = op_str + " " + str(random_num)
        if rand_op == 4:
            op_str = op_str + " at index " + str(rand_index)
if validity_failure:
    failed_tests.append("RANDOM TEST")
    validity_failure = False

# Sixth test: perform a series of random searches on last list created

print("\nRANDOM SEARCHES, seed={}".format(random_seed))
# Now add some more random numbers
for i in range(10):
    random_num = random.randrange(10000)
    rand_ll.add_tail(random_num)
    python_list.append(random_num)
print("linked list", rand_ll.get_items())
print("python list", python_list)

for i in range(10):
    rand_index = random.randrange(rand_ll.size())
    old_cached_index = rand_ll.cached_ref.idx
    item = rand_ll.get_item(rand_index)
    if verbosity > 0:
        print("Item at {} is:".format(rand_index), item, "cached index moves from {} to {}".format(old_cached_index, rand_ll.cached_ref.idx))
    else:
        print("Item at {} is:".format(rand_index), item)
    valid, error_str = rand_ll.validate()
    if not valid:
        print("Validity error:", error_str)
        validity_failure = True
    # make sure that retrieved item matches item in python list
    if python_list[rand_ll.cached_ref.idx] != item:
        print("Cache index is wrong")
        validity_failure = True
if validity_failure:
    failed_tests.append("RANDOM SEARCHES")
    validity_failure = False

print("\nSORTING")
sort_ll = TestList(['h', 'b', 'j', 'e', 'a', 'c', 'f', 'd', 'g', 'i'])
print("pre-sorted:", sort_ll.get_items())
sort_ll.sort()
sorted_items = sort_ll.get_items()
print("sorted to:", sorted_items)
sorted_python_rand_list = rand_ll.get_items()
sorted_python_rand_list.sort()
rand_ll.sort(expected_list=sorted_python_rand_list)
print("sorted rand list:", rand_ll.get_items())
sorted_python_rand_list.sort(reverse=True)
rand_ll.sort(reverse=True, expected_list=sorted_python_rand_list)
print("sorted rand list, reverse:", rand_ll.get_items())
if validity_failure:
    failed_tests.append("SORTING")
    validity_failure = False

print("\nJOINING")
join_list1 = TestList(["elephant", "giraffe", "hippo"])
join_list2 = TestList(["gazelle", "rhinoceros"])
print("join list 1:", join_list1.get_items())
print("join list 2:", join_list2.get_items())
join_list1.join(join_list2, expected_list=["elephant", "giraffe", "hippo", "gazelle", "rhinoceros"])
print("new join list 1:", join_list1.get_items())
print("new join list 2:", join_list2.get_items())
join_list2.join(join_list1, expected_list=["elephant", "giraffe", "hippo", "gazelle", "rhinoceros"])
if validity_failure:
    failed_tests.append("JOINING")
    validity_failure = False

print("\nSPLITTING")
print("split list:", join_list2.get_items())
split_off_list = join_list2.split(2, expected_list=["elephant", "giraffe"])
print("split-off list:", split_off_list.get_items())
print("remaining list:", join_list2.get_items())
split_off_list2 = join_list2.split(2)
split_off_list2.add_tail("bat")
join_list2.join(split_off_list2, expected_list=["elephant", "giraffe", "bat"])
split_off_list.join(TestList(["meerkat"]), expected_list=["hippo", "gazelle", "rhinoceros", "meerkat"])
big_combined_list = join_list2.copy()
big_combined_list.join(split_off_list, expected_list=["elephant", "giraffe", "bat", "hippo", "gazelle", "rhinoceros", "meerkat"])
if validity_failure:
    failed_tests.append("SPLITTING")
    validity_failure = False

if len(failed_tests) > 0:
    # If we don't get into this block of code, all tests were successful. If we do, we see a printout of which ones
    # failed
    print("")
    print("FAILED TESTS")
    for t in failed_tests:
        print(t)

