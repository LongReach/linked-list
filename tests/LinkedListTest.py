import random
import time
import argparse
import linked_list.test_list as tl

parser = argparse.ArgumentParser(description='Tester program for LinkedListClass.')
parser.add_argument("--verbosity", help="Verbosity level (0=verbose, 1=semi-verbose, 2=silent)", type=int, default=1)
parser.add_argument("--seed", help="A seed for random number generation (to reproduce same tests)", type=int, default=-1)
parser.add_argument("--test", help="Number of test to run (don't specify to run all)", type=int, default=-1)
args = parser.parse_args()

verbosity = args.verbosity
random_seed = args.seed

if random_seed == -1:
    # choose a seed at random (sort of)
    random_seed = int(time.time()) % 100000
random.seed(random_seed)

failed_tests = []
default_tests = ["BASIC TEST A", "BASIC TEST B", "BASIC TEST C", "FIND TEST", "RANDOM TEST", "RANDOM SEARCH",
                 "SORTING", "JOINING", "SPLITTING", "ITERATOR"]
tests_to_run = set()
if args.test == -1:
    for i in range(len(default_tests)):
        tests_to_run.add(i+1)
else:
    tests_to_run.add(args.test)

def should_run_test(test_num):
    if test_num in tests_to_run:
        print("\nRunning test {}: {}".format(test_num, default_tests[test_num-1]))
        return True
    return False

def handle_test_failure(test_num):
    global failed_tests
    if tl.validity_failure:
        print("FAILED TEST:", default_tests[test_num-1])
        failed_tests.append(default_tests[test_num-1])
        tl.validity_failure = False

# First test: a few simple operations on a predefined linked list

if should_run_test(1):
    words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]
    callsign_ll = tl.TestList(words)
    callsign_ll.verbosity = verbosity
    callsign_ll.test_new_cache_item(3)
    callsign_ll.reverse_list()
    callsign_ll.reverse_list()
    callsign_ll.pop_head()
    callsign_ll.pop_tail(expected_list=['bravo', 'charlie', 'delta', 'echo'])
    callsign_ll.add_head("A")
    callsign_ll.add_tail("F")
    handle_test_failure(1)

# Second test: a few simple operations on another predefined linked list

if should_run_test(2):
    number_ll = tl.TestList()
    number_ll.verbosity = verbosity
    number_ll.add_head("two")
    number_ll.add_head("one")
    number_ll.test_new_cache_item(0)
    number_ll.pop_head()
    number_ll.pop_head(expected_list=[])
    number_ll.add_head("zzz", expected_list=["zzz"])
    handle_test_failure(2)

# Third test: more list modifications. Also, we try searches for indices NOT in the list.

if should_run_test(3):
    fruit_ll = tl.TestList(["apple", "orange", "pear", "banana", "grape", "lemon", "lime", "grapefruit"])
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
            print("did not get exception for index-out-of-range test, as expected")
            tl.validity_failure = True
    handle_test_failure(3)

# Fourth test: perform finds on same list as last test. Some finds are expected to succeed, others to fail

if should_run_test(4):
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
                    tl.validity_failure = True
                    print("failed find for {} where success was expected".format(f[0]))
            else:
                if find_list is fail_finds:
                    tl.validity_failure = True
                    print("successful find for {} where failure was expected".format(f[0]))
    handle_test_failure(4)

# Fifth test:
# This test creates an empty list, then performs a series of random operations on it, putting in random numbers
# At the same time, we perform the same operations on a regular Python list, which we compare to the linked list.

if should_run_test(5):
    print("seed={}".format(random_seed))
    rand_ll = tl.TestList()
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
    handle_test_failure(5)

# Sixth test: perform a series of random searches on last list created

if should_run_test(6):
    print("seed={}".format(random_seed))
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
            tl.validity_failure = True
        # make sure that retrieved item matches item in python list
        if python_list[rand_ll.cached_ref.idx] != item:
            print("Cache index is wrong")
            tl.validity_failure = True
    handle_test_failure(6)

if should_run_test(7):
    sort_ll = tl.TestList(['h', 'b', 'j', 'e', 'a', 'c', 'f', 'd', 'g', 'i'])
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
    handle_test_failure(7)

if should_run_test(8):
    join_list1 = tl.TestList(["elephant", "giraffe", "hippo"])
    join_list2 = tl.TestList(["gazelle", "rhinoceros"])
    print("join list 1:", join_list1.get_items())
    print("join list 2:", join_list2.get_items())
    join_list1.join(join_list2, expected_list=["elephant", "giraffe", "hippo", "gazelle", "rhinoceros"])
    print("new join list 1:", join_list1.get_items())
    print("new join list 2:", join_list2.get_items())
    join_list2.join(join_list1, expected_list=["elephant", "giraffe", "hippo", "gazelle", "rhinoceros"])
    handle_test_failure(8)

if should_run_test(9):
    print("split list:", join_list2.get_items())
    split_off_list = join_list2.split(2, expected_list=["elephant", "giraffe"])
    print("split-off list:", split_off_list.get_items())
    print("remaining list:", join_list2.get_items())
    split_off_list2 = join_list2.split(2)
    split_off_list2.add_tail("bat")
    join_list2.join(split_off_list2, expected_list=["elephant", "giraffe", "bat"])
    split_off_list.join(tl.TestList(["meerkat"]), expected_list=["hippo", "gazelle", "rhinoceros", "meerkat"])
    big_combined_list = join_list2.copy()
    big_combined_list.join(split_off_list, expected_list=["elephant", "giraffe", "bat", "hippo", "gazelle", "rhinoceros", "meerkat"])
    handle_test_failure(9)

if should_run_test(10):
    iterated_items = []
    indices = []
    for n,item in enumerate(fruit_ll):
        indices.append(n)
        iterated_items.append(item)
    print("iterated items are:", iterated_items)
    print("indices:", indices)
    if not fruit_ll.compare(['tomato', 'apple', 'orange', 'pear', 'coconut', 'banana', 'grape', 'lemon', 'lime', 'grapefruit']):
        tl.validity_failure = True
    handle_test_failure(10)

if len(failed_tests) > 0:
    # If we don't get into this block of code, all tests were successful. If we do, we see a printout of which ones
    # failed
    print("")
    print("FAILED TESTS")
    for t in failed_tests:
        print(t)

