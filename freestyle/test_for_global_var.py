from freestyle.collections import globals_manager


class module:
    pass


block = module()
globals_manager(global_vars=block.__dict__)

from freestyle.collections import richIterator
from collections import deque


class richList(richIterator, list):
    pass


class richDeque(richIterator, deque):
    pass


from numpy.random import rand
rdq = richDeque(rand(15))
print(rdq.groupBy(lambda x: x // 0.1))
print(rdq@(lambda x: sum(x.filter(lambda each: each >= 0.5))))
print(rdq.filter(lambda x: 0.3 < x < 0.35).let(this="this", origin=rdq).then(
    lambda x, y: x.tolist() + y.tolist(), block.this, block.origin))
rdq = richList([1, 2, 3])
rdq.let(c=rdq.map(lambda x: x * 2)
        )@(lambda x: x.map(lambda x, y: x * y, block.c).tolist)
rdq.let(c=2).map(lambda x: block.c * x).totuple()
print(type(rdq.map(lambda x: x + 1)))
