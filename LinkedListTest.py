import random
from linked_list import LinkedList

validity_failure = False

def print_list_details(the_list, operation=None):
    global validity_failure
    valid, error_str = the_list._validate()
    if operation is not None:
        print("operation:", operation)
    print("list is:", the_list.get_items())
    print("    length is:", the_list.size())
    print("    cached index:", the_list.cached_index)
    print("    cached item:", "NONE" if the_list.cached_node is None else the_list.cached_node.item)
    if not valid:
        validity_failure = True
        print("    *** validity failed ***, error code:", error_str)
    print("--------------------")

print("")
print("LIST ONE")
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

print("")
print("LIST TWO")
ll2 = LinkedList()
ll2.add_head("two")
ll2.add_head("one")
ll2._new_cache_item(0)
print_list_details(ll2)
ll2.pop_head()
print_list_details(ll2, "pop head")
ll2.pop_head()
print_list_details(ll2, "pop head")
ll2.add_head("zzz")
print_list_details(ll2, "add head")

print("")
print("LIST THREE")
ll3 = LinkedList(["apple", "orange", "pear", "banana", "grape", "lemon", "lime", "grapefruit"])
ll3.get_item(2)
print_list_details(ll3, "get item 2")
ll3.get_item(5)
print_list_details(ll3, "get item 5")
ll3.get_item(3)
print_list_details(ll3, "get item 3")
ll3.insert("coconut", 3)
print_list_details(ll3, "insert")
ll3.insert("tomato", 0)
print_list_details(ll3, "insert")
try:
    ll3.get_item(17)
except IndexError:
    print("index out of range, as expected")

print("")
print("LIST RANDOM TEST")
rand_list = LinkedList()
for i in range(20):
    random_num = random.randrange(10000)
    operations = ["add_head", "add_tail", "pop_head", "pop_tail", "insert"]
    rand_op = random.randrange(5)
    rand_index = 0
    if rand_op == 0:
        rand_list.add_head(random_num)
    elif rand_op == 1:
        rand_list.add_tail(random_num)
    elif rand_op == 2:
        rand_list.pop_head()
    elif rand_op == 3:
        rand_list.pop_tail()
    elif rand_op == 4:
        rand_index = 0 if rand_list.size() == 0 else random.randrange(rand_list.size())
        rand_list.insert(random_num, rand_index)
    op_str = operations[rand_op]
    if rand_op == 0 or rand_op == 1 or rand_op == 4:
        op_str = op_str + " " + str(random_num)
        if rand_op == 4:
            op_str = op_str + " at index " + str(rand_index)
    print_list_details(rand_list, op_str)

if validity_failure:
    print("")
    print("VALIDITY FAILURE")

print("")
print("LIST RANDOM SEARCHES")

# Now add some more random numbers
for i in range(10):
    random_num = random.randrange(10000)
    rand_list.add_tail(random_num)
print_list_details(rand_list)

for i in range(10):
    rand_index = random.randrange(rand_list.size())
    item = rand_list.get_item(rand_index)
    print("Item at {} is:".format(rand_index), item)
    valid, error_str = rand_list._validate()
    if not valid:
        print("Validity error:", error_str)
