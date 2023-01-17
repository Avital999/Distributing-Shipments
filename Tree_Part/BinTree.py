import numpy as np
from eckity.individual import Individual
import random


class BinNode:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.parent = None
        self.val = val
        self.height = None
        self.size = None

    def changeVal(self, newVal):
        self.val = newVal

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def switch_left_and_right(self):
        temp_node = self.left
        self.left = self.right
        self.right = temp_node

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def _display_aux(self):
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.val
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.val
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def updateHeightAndSize(node, height):
    node.height = height
    node = node.parent
    while node is not None:
        node.size += 1
        height = height + 1
        if node.height < height:
            node.height = height
        node = node.parent


def subTreeIsFull(node):
    if node is None:
        return False
    return node.size == ((2 ** (node.height + 1)) - 1)


# implementation of complete binary tree


class BinTree(Individual):
    def __init__(self, fitness):
        super().__init__(fitness)
        self.root = None

    def get_root(self):
        return self.root

    def size(self):
        return self.root.size

    def add(self, val):
        if self.root is None:
            self.root = BinNode(val)
            self.root.height = 0
            self.root.size = 1
            self.root.parent = None
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if node.right is None:
            node.right = BinNode(val)
            node.right.parent = node
            node.right.size = 1
            updateHeightAndSize(node.right, 0)
        elif node.left is None:
            node.left = BinNode(val)
            node.left.parent = node
            node.left.size = 1
            updateHeightAndSize(node.left, 0)
        elif node.left.height == node.right.height and not (subTreeIsFull(node.left)):
            self._add(val, node.left)
        elif node.left.height + 1 == node.right.height and subTreeIsFull(node.right):
            self._add(val, node.left)
        else:
            self._add(val, node.right)

    def find(self, val):
        if self.root is not None:
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        if val == node.val:
            return node
        else:
            if node.right is None:
                return None
            find_right = self._find(val, node.right)
            if node.left is None:
                return None
            if find_right is None:
                return self._find(val, node.left)
            else:
                return find_right

    def deleteTree(self):
        # garbage collector will do this for us.
        self.root = None

    def printTree(self):
        if self.root is not None:
            self._printTree(self.root)

    def _printTree(self, node):
        self.root.display()

    def inOrder(self, node):
        res = []
        if node is not None:
            left = []
            if node.left is not None:
                left.extend(self.inOrder(node.left))
            left.extend(res)
            res = left
            res.append(node.val)
            res.extend(self.inOrder(node.right))
        return res

    def randomSubtree(self):
        node = self.root
        if node is not None:
            h = node.height
            r = int((h + 1) / 3 + 0.5)
            stop = False
            while not stop:
                if random.random() > 0.5:
                    if node.right.height >= r:
                        node = node.right
                    else:
                        node = node.left
                else:
                    if node.left.height >= r:
                        node = node.left
                    else:
                        node = node.right
                if node.height <= r:
                    stop = True
        return node

    def replace_subtree(self, subtree):
        rand = self.randomSubtree()
        curr = self.inOrder(rand)
        sub = self.inOrder(subtree)

        # save number of change courier in current subtree and in new subtree
        curr_num_change = curr.count("Change courier")
        sub_num_change = sub.count("Change courier")

        # separate packages from all nodes in curr-subtree and new subtree
        # filter curr
        curr_packages = []
        for element in curr:
            if element != "Change courier" and element != "Keep going":
                if element not in sub:
                    curr_packages.append(element)
        # go over packages in new subtree
        for element in sub:
            if element != "Change courier" and element != "Keep going":
                if element not in curr:
                    if curr_packages:
                        el_in_curr = self.find(element)
                        old_val = curr_packages.pop()
                        old_node = self.find(old_val)
                        # replace node with val element in current tree with curr packages value - old val
                        el_in_curr.changeVal(old_val)
                        # replace rand subtree with value - old_val with element value
                        old_node.changeVal(element)

        # update "Change courier" in new tree
        changes = curr_num_change - sub_num_change
        # if new subtree has more "Change courier" than old tree replace them in keep going
        while changes < 0:
            node = self.find("Change courier")
            if node is not None:
                node.changeVal("Keep going")
            changes = changes +1
        # if old subtree had more "Change courier" than new subtree add "Change courier" to subtree
        while changes > 0:
            node = self._find("Keep going", rand)
            if node is not None:
                node.changeVal("Change courier")
            changes = changes - 1



    def show(self):
        self.printTree()
        print(self.inOrder(self.root))
