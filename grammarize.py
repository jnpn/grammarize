#!/usr/bin/env python

from functools import partial

def flatten(l):
    r = []
    for e in l:
        if type(e) is not list:
            r.append(e)
        else:
            r.extend(flatten(e))
    return r

# flatten([])      -> []
# flatten([1])     -> [1]
# flatten([1 2])   -> [1 2]
# flatten([[1]])   -> [1]
# flatten([[1] 2]) -> [1 2]
# flatten([1 [2]]) -> [1 2]

def flatmap(f,l):
    return flatten(map(f,l))

# tree a -> (value a, left tree, right tree)
# t = (1 (2 None None) None)

class Tree:

    def __init__(self, n, l=None, r=None):
        self.n = n
        self.l = l
        self.r = r

    def node(self):
        return self.n

    def left(self):
        return self.l

    def right(self):
        return self.r

    def isleaf(self):
        return self.left() is None and self.right() is None

    def children(self):
        return [self.left(), self.right()]

    def __repr__(self):
        if self.isleaf():
            return '(Leaf %s)' % (self.node())
        else:
            return '(Tree %s %s %s)' % (self.node(), self.left(), self.right())
    
    def walk(self):
        """Tree -> [Tree]
        TOFIX: fails on non binary trees
        """
        # case leaf -> [Tree]
        if self.isleaf():
            return [self]
        # case tree -> [Tree]
        else:
            # t (+) walk left (+) walk right
            return [self] + self.left().walk() + self.right().walk()

t0 = Tree('body',
          Tree('div'),
          Tree('div'))

t1 = Tree('body',
          Tree('div'),
          Tree('div', Tree('wat',
                           Tree('duh'),
                           Tree('eww'))))

t2 = Tree('body',
          Tree('ldiv'),
          Tree('rdiv',
               Tree('lwat',
                    Tree('lduh'),
                    Tree('leww')),
               Tree('rwat',
                    Tree('rduh'),
                    Tree('reww'))))

t3 = Tree('body',
          Tree('pre'),
          Tree('div',
               Tree('p',
                    Tree('h1'),
                    Tree('span')),
               Tree('p',
                    Tree('h2'),
                    Tree('a'))))


def wrappend(l,v):
    c = l.copy()
    c.append(v)
    return c

class Gree(Tree):

    from itertools import groupby

    def rules_(self):
        return list((self.node(),TreeChildrenNames(t)) # ???
                    for t in self.walk()
                    if not self.isleaf())

    def rules__(self):
        # clean: [(tag, [subtag])] -> Union [subtag]
        def clean(l):
            return set(flatten([s for e,s in l]))
        return list((p, clean(cs)) for p,cs in groupby(self.rules_(), self.node))

    def rules(self):
        return dict(self.rules__())

# grammarize Tree -> Grammar
#
# Tree -{treewalk}-> [(Node, Children)] -{merge}-> [(Node, Children)]'
#
# merge [(n,c0), (n, c1), ...] -> [(n, (union c0 c1))]
