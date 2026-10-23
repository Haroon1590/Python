"""Shared fixtures + execution-order control for the whole suite."""
import pytest

# Group execution order (first = runs first). A test belongs to the FIRST group
# in this list that it is marked with.
GROUP_ORDER = ["smoke", "ecp", "bva", "negative", "scenario", "csv_driven"]
GROUP_STEP = 100          # gap between groups
DEFAULT_CASE_ORDER = 50   # position inside a group unless @pytest.mark.case_order(n)


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Give every test a pytest-order number = group slot + case slot."""
    for item in items:
        group_idx = len(GROUP_ORDER)
        for idx, name in enumerate(GROUP_ORDER):
            if item.get_closest_marker(name):
                group_idx = idx
                break
        case = item.get_closest_marker("case_order")
        case_no = case.args[0] if case else DEFAULT_CASE_ORDER
        item.add_marker(pytest.mark.order((group_idx + 1) * GROUP_STEP + case_no))


@pytest.fixture
def make_stack():
    """make_stack(limit=10, ops="ppx"): 'p' pushes 1,2,3.. ; 'x' pops."""
    from data_structures.stacks.stack import Stack

    def _make(limit=10, ops=""):
        s, n = Stack(limit), 0
        for op in ops:
            if op == "p":
                n += 1
                s.push(n)
            elif op == "x":
                s.pop()
            else:
                raise ValueError(f"unknown op {op!r}")
        return s

    return _make


@pytest.fixture
def make_queue():
    """make_queue(n=5, ops="eed"): 'e' enqueues 'A','B',.. ; 'd' dequeues."""
    from data_structures.queues.circular_queue import CircularQueue

    def _make(n=5, ops=""):
        q, k = CircularQueue(n), 0
        for op in ops:
            if op == "e":
                k += 1
                q.enqueue(chr(64 + k))
            elif op == "d":
                q.dequeue()
            else:
                raise ValueError(f"unknown op {op!r}")
        return q

    return _make
