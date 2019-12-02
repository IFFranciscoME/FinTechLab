
import queue as queue

import numpy


class Nodo:
    def __init__(self, value, left=None, right=None, ismin=False):
        self.value = value
        self.left = left
        self.right = right
        self.ismin = ismin


class Tree:
    def __init__(self, value=None):
        self.nodo = Nodo(value)

    def generateminmax(self, values):
        auxqueue = queue.SimpleQueue()
        current = self.nodo
        counter = 1
        for val in values:
            level = numpy.floor(numpy.log2(counter)) + 1
            ismin = level % 2 == 0
            if not current.value:
                current.value = val
                current.isMin = ismin
            elif not current.left:
                current.left = Nodo(val, ismin=ismin)
                auxqueue.put(current.left)
            elif not current.right:
                current.right = Nodo(val, ismin=ismin)
                auxqueue.put(current.right)
                current = auxqueue.get()
            counter = counter + 1


tree = Tree()
tree.generateminmax([10, 4, 5, 10, 3, 42, 3, 2, 3, 4, 10, 3, 5, 6, 10])
