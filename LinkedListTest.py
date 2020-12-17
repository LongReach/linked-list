import random
import time
import argparse
from linked_list import LinkedList

parser = argparse.ArgumentParser(description='Tester program for LinkedListClass.')
parser.add_argument("-v", "--verbose", help="If set, print extra info", action="store_true")
parser.add_argument("--seed", help="A seed for random number generation (to reproduce same tests)", type=int, default=-1)
args = parser.parse_args()

validity_failure = False
failed_tests = []
verbose_test = args.verbose
random_seed = args.seed

if random_seed == -1:
    # choose a seed at random (sort of)
    random_seed = int(time.time()) % 100000
random.seed(random_seed)


# Given a linked list, print information about it, validate the list, and compare to contents of a Python list
# last_operation_str: string containing name of last last_operation_str
# expected_list: if set, a Python list containing expected results of last last_operation_str
def examine_list_details(the_list, last_operation_str=None, expected_list=None):
    global validity_failure
    valid, error_str = the_list._validate()
    if last_operation_str is not None:
        print("last_operation_str:", last_operation_str)
    if verbose_test:
        print("list is:", the_list.get_items())
        print("    length is:", the_list.size())
        print("    cached index:", the_list.cached_ref.idx)
        print("    cached item:", "NONE" if the_list.cached_ref.empty() else the_list.cached_ref.node.item)
    if not valid:
        validity_failure = True
        print("    *** validity failed ***, error code:", error_str)
    if expected_list is not None:
        match = True
        the_items = the_list.get_items()
        if len(expected_list) != len(the_items):
            match = False
        else:
            for i, item in enumerate(expected_list):
                if expected_list[i] != the_items[i]:
                    match = False
        if not match:
            validity_failure = True
            print("    *** expected result failure ***:", expected_list)
    if verbose_test:
        print("--------------------")

print("")
print("TEST ONE")
words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]
callsign_ll = LinkedList(words)
callsign_ll._new_cache_item(3)
examine_list_details(callsign_ll, "new list, cache item 3")
callsign_ll.reverse_list()
examine_list_details(callsign_ll, "reversed")
callsign_ll.reverse_list()
callsign_ll.pop_head()
examine_list_details(callsign_ll, "popped head")
callsign_ll.pop_tail()
examine_list_details(callsign_ll, "popped tail", ['bravo', 'charlie', 'delta', 'echo'])
callsign_ll.add_head("A")
examine_list_details(callsign_ll, "added head")
callsign_ll.add_tail("F")
examine_list_details(callsign_ll, "added tail")
if validity_failure:
    failed_tests.append("TEST ONE")
    validity_failure = False

print("")
print("TEST TWO")
number_ll = LinkedList()
number_ll.add_head("two")
number_ll.add_head("one")
number_ll._new_cache_item(0)
examine_list_details(number_ll)
number_ll.pop_head()
examine_list_details(number_ll, "pop head")
number_ll.pop_head()
examine_list_details(number_ll, "pop head", expected_list=[])
number_ll.add_head("zzz")
examine_list_details(number_ll, "add head")
if validity_failure:
    failed_tests.append("TEST TWO")
    validity_failure = False

print("")
print("TEST THREE")
fruit_ll = LinkedList(["apple", "orange", "pear", "banana", "grape", "lemon", "lime", "grapefruit"])
fruit_ll.get_item(2)
examine_list_details(fruit_ll, "get item 2")
fruit_ll.get_item(5)
examine_list_details(fruit_ll, "get item 5")
fruit_ll.get_item(3)
examine_list_details(fruit_ll, "get item 3")
fruit_ll.insert("coconut", 3)
examine_list_details(fruit_ll, "insert", ['apple', 'orange', 'pear', 'coconut', 'banana', 'grape', 'lemon', 'lime', 'grapefruit'])
fruit_ll.insert("tomato", 0)
examine_list_details(fruit_ll, "insert", ['tomato', 'apple', 'orange', 'pear', 'coconut', 'banana', 'grape', 'lemon', 'lime', 'grapefruit'])
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

print("")
print("FIND TEST")
# We should have: ['tomato', 'apple', 'orange', 'pear', 'coconut', 'banana', 'grape', 'lemon', 'lime', 'grapefruit']
# Each tuple: item, start index, reverse
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

# This test creates an empty list, then performs a series of random operations on it, putting in random numbers
# At the same time, we perform the same operations on a regular Python list, which we compare
print("")
print("RANDOM TEST: seed={}".format(random_seed))
rand_ll = LinkedList()
python_list = []
for i in range(20):
    random_num = random.randrange(10000)
    operations = ["add_head", "add_tail", "pop_head", "pop_tail", "insert"]
    rand_op = random.randrange(5)
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
    op_str = operations[rand_op]
    if rand_op == 0 or rand_op == 1 or rand_op == 4:
        op_str = op_str + " " + str(random_num)
        if rand_op == 4:
            op_str = op_str + " at index " + str(rand_index)
    examine_list_details(rand_ll, op_str, python_list)
if validity_failure:
    failed_tests.append("RANDOM TEST")
    validity_failure = False

print("")
print("RANDOM SEARCHES, seed={}".format(random_seed))
# Now add some more random numbers
for i in range(10):
    random_num = random.randrange(10000)
    rand_ll.add_tail(random_num)
    python_list.append(random_num)
examine_list_details(rand_ll, expected_list=python_list)
print("linked list", rand_ll.get_items())
print("python list", python_list)

for i in range(10):
    rand_index = random.randrange(rand_ll.size())
    old_cached_index = rand_ll.cached_ref.idx
    item = rand_ll.get_item(rand_index)
    if verbose_test:
        print("Item at {} is:".format(rand_index), item, "cached index moves from {} to {}".format(old_cached_index, rand_ll.cached_ref.idx))
    else:
        print("Item at {} is:".format(rand_index), item)
    valid, error_str = rand_ll._validate()
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

if len(failed_tests) > 0:
    print("")
    print("FAILED TESTS")
    for t in failed_tests:
        print(t)

