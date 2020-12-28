from itertools import islice, takewhile


class LinkedListNode(object):
    next = None
    value = None

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        next = None if self.next is None else self.next.value
        return f"<LLNode {self.value} {next}>"


def create_circular_linked_list(vals):
    nodes = (LinkedListNode(val) for val in vals)
    head = prev = next(nodes)
    for node in nodes:
        prev.next = node
        yield prev
        prev = node
    node.next = head
    yield node


def iterate_linked_list(head: LinkedListNode):
    node = head
    while node:
        yield node
        node = node.next


def find_tail(head):
    node = head
    while node.next:
        if node.next == head:
            raise Exception("Circular list detected")
        node = node.next
    return node


def iterate_circular_linked_list(head: LinkedListNode):
    yield head
    # iterate_linked_list will cycle a circular list infinitely, so stop when we hit head again
    it = iterate_linked_list(head.next)
    yield from takewhile(lambda node: node != head, it)


def linked_list_extract(head, n):
    extraction = extraction_tail = head.next
    for i in range(n-1):
        extraction_tail = extraction_tail.next
    head.next = extraction_tail.next
    extraction_tail.next = None
    return extraction


def linked_list_insert(head, insert):
    tail = head.next
    head.next = insert
    find_tail(insert).next = tail


def find_destination_cup(lookup, picked_up, start_val, max_value):
    picked_up_values = set([node.value for node in iterate_circular_linked_list(picked_up)])

    # Our list is 1 based, so subtract two then mod then add 1, so 0 wraps to max_value
    lookup_val = (start_val - 2) % max_value + 1
    while lookup_val in picked_up_values:
        lookup_val = (lookup_val - 2) % max_value + 1

    return lookup[lookup_val]


def shuffle_cups(vals):
    nodes = create_circular_linked_list(vals)
    lookup = {node.value: node for node in nodes}
    max_value = max(vals)
    current = lookup[vals[0]]

    while True:
        yield lookup

        picked_up = linked_list_extract(current, 3)
        destination = find_destination_cup(lookup, picked_up, current.value, max_value)

        linked_list_insert(destination, picked_up)

        current = lookup[current.value].next


def render_cups(lookup):
    # Center on 1
    center = lookup[1]
    it = iterate_circular_linked_list(center)
    next(it)
    return "".join(str(node.value) for node in it)


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    v = next(islice(iterable, n, None), default)
    return v


def expand_cups(lst):
    return lst + list(range(max(lst)+1, 1000001))


assert render_cups(nth(shuffle_cups([3, 8, 9, 1, 2, 5, 4, 6, 7]), 10)) == "92658374"
assert render_cups(nth(shuffle_cups([3, 8, 9, 1, 2, 5, 4, 6, 7]), 100)) == "67384529"


with open("./data.txt", "r") as fp:
    vals = [int(v) for v in fp.read().strip()]

vals = expand_cups(vals)

final_state = nth(shuffle_cups(vals), 10000000)
print(final_state[1].next.value * final_state[1].next.next.value)
