## linked-list

**A Python Implementation of a Linked List**

## Overview

Python has lists, obviously, but they're really arrays under the hood. I decided to try my hand at creating a proper linked list class, one with the traditional advantages of linked lists, such as fast insertion or removal operations. I'm sure I was reinventing the wheel, but this was still a worthwhile exercise for me.

I also created a test framework, which takes advantage of Python decorators. The test module creates a series of linked lists and performs various operations on them. At each step, the decorator function makes sure the list is valid.

One test involves performing random operations on a linked list, while mirroring the same operations with a regular Python list. At the end of the sequence, the linked list and the regular list are compared.

Feel free to use this code.

## Design

![](images/DoubleLinkedList.png) 

This is a doubly-linked list, as shown above. It does many of the common things we would want a linked list class to be able to do.

One innovation I added is the concept of a node cache. That is, the linked list maintains a cache of select nodes that it remembers the indices of. Periodically, the cache is rebuilt, with the cached nodes distributed more or less evenly across the whole list. Thus, if the caller wants the item at a particular index, it's not necessary to iterate through the entire linked list. Rather, the cache is searched for a node close to the desired one and iteration happens from there.

## Operations

#### Finding

![](images/IsItMeYoureLookingFor.jpg) 

* get item (by index)
* find item (by value)

#### Adding

* add head (add to front of list)
* add tail
* insert (at arbitrary index)

#### Removing

* pop head
* pop tail
* remove (from arbitrary index)

#### Whole List

* clear
* copy
* reverse
* sort
* join (combine two lists into one)
* split (split a list into two lists)

#### Iterator

![](images/PythonIterator.jpg)

The linked list can be iterated through in the standard Python way:
 
```
for item in linked_list:
    # do something
```

Or

```
for n,item in enumerate(linked_list):
    # do something
```

## Installation

Download the whole package, then install from the top-level folder as follows:

`D:\CodingProjects\Python\LinkedList>python scripts\linked_list>pip install .`

## Running Tests

![](images/GrenadeMonkey.jpg)

`Unit-testing before going live is usually wise`

Run with:

(Windows)   
`D:\CodingProjects\Python\LinkedList>python scripts\linked_list>python scripts\linked_list --verbosity CODE --seed RANDOMSEED --test TESTNUM --help`

(Linux-y)  
`$ linked_list --verbosity CODE --seed RANDOMSEED --test TESTNUM --help`

Argument | Description
---------|------------
`help` | Print help
`verbosity` | Level of verbosity: 0 to 2. 2 is most verbose.
`seed` | A seed for random number generation. Use same seed for repeatable results.
`test` | Which test to run (don't specify to run all)

## Sample Output

A few tests, less verbose output:

```
Running test 7: SORTING
pre-sorted: ['h', 'b', 'j', 'e', 'a', 'c', 'f', 'd', 'g', 'i']
sorted to: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
sorted rand list: [563, 568, 935, 1561, 2506, 3280, 6101, 6175, 9693, 9765]
sorted rand list, reverse: [9765, 9693, 6175, 6101, 3280, 2506, 1561, 935, 568, 563]

Running test 8: JOINING
join list 1: ['elephant', 'giraffe', 'hippo']
join list 2: ['gazelle', 'rhinoceros']
new join list 1: ['elephant', 'giraffe', 'hippo', 'gazelle', 'rhinoceros']
new join list 2: []

Running test 9: SPLITTING
split list: ['elephant', 'giraffe', 'hippo', 'gazelle', 'rhinoceros']
split-off list: ['hippo', 'gazelle', 'rhinoceros']
remaining list: ['elephant', 'giraffe']
```

A few random operations, involving random data. More verbose output.

```
RANDOM TEST: seed=54217
last_operation_str: pop_head
list is: []
    length is: 0
    cached index: -1
    cached item: NONE
--------------------
last_operation_str: add_head, item=9458
list is: [9458]
    length is: 1
    cached index: 0
    cached item: 9458
--------------------
last_operation_str: add_tail, item=4619
list is: [9458, 4619]
    length is: 2
    cached index: 0
    cached item: 9458
--------------------
last_operation_str: add_head, item=2845
list is: [2845, 9458, 4619]
    length is: 3
    cached index: 1
    cached item: 9458
--------------------
last_operation_str: add_head, item=2845
list is: [2845, 9458, 4619]
    length is: 3
    cached index: 1
    cached item: 9458
--------------------
last_operation_str: pop_tail
list is: [2845, 9458]
    length is: 2
    cached index: 1
    cached item: 9458
--------------------
last_operation_str: insert, item=9493 at 1
list is: [2845, 9493, 9458]
    length is: 3
    cached index: 1
    cached item: 9493
--------------------
last_operation_str: insert, item=9245 at 1
list is: [2845, 9245, 9493, 9458]
    length is: 4
    cached index: 1
    cached item: 9245
--------------------
```
...
snipped
...
```
linked list [1274, 2845, 9245, 9493, 4743, 4949, 2069, 9673, 3226, 6419, 5021, 9050, 9103, 6787, 9332]
python list [1274, 2845, 9245, 9493, 4743, 4949, 2069, 9673, 3226, 6419, 5021, 9050, 9103, 6787, 9332]
```