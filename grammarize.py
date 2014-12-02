#!/usr/bin/env python

from itertools import groupby

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

    def maybe(self,v,f,p,d):
        return f(v) if p(v) else d

    def mayli(self,v,f):
        return self.maybe(v, f, lambda v: v is not None, [])

    def mhildren(self):
        listify = lambda e: [e]
        maybeleft  = self.mayli(self.left(), listify)
        mayberight  = self.mayli(self.right(), listify)
        return [] + maybeleft + mayberight

    def children_names(self):
        return [c.node() for c in self.mhildren()]

    def __repr__(self):
        if self.isleaf():
            return '(Leaf %s)' % (self.node())
        else:
            return '(Tree %s %s %s)' % (self.node(), self.left(), self.right())
    
    def walk(self):
        """Tree -> [Tree]
        """
        # t (+) default walk left (+) default walk right
        walkify = lambda e: e.walk()
        maybeleft  = self.mayli(self.left(), walkify)
        mayberight  = self.mayli(self.right(), walkify)
        return [self] + maybeleft + mayberight

class Gree(Tree):

    def rules_(self):
        return list((t.node(),t.children_names())
                    for t in self.walk()
                    if not t.isleaf())

    def rules__(self):
        # clean: [(tag, [subtag])] -> Union [subtag]
        def clean(l):
            return set(flatten([s for e,s in l]))
        parent_name = lambda t: t[0]
        return list((p, clean(cs)) for p,cs in groupby(self.rules_(), parent_name))

    def rules(self):
        return dict(self.rules__())

### Tests

t0 = Gree('body',
          Gree('div'),
          Gree('div'))

t1 = Gree('body',
          Gree('div'),
          Gree('div', Gree('wat',
                           Gree('duh'),
                           Gree('eww'))))

t2 = Gree('body',
          Gree('ldiv'),
          Gree('rdiv',
               Gree('lwat',
                    Gree('lduh'),
                    Gree('leww')),
               Gree('rwat',
                    Gree('rduh'),
                    Gree('reww'))))

t3 = Gree('body',
          Gree('pre'),
          Gree('div',
               Gree('p',
                    Gree('h1'),
                    Gree('span')),
               Gree('p',
                    Gree('h2'),
                    Gree('a'))))

g3 = Gree('body',
          Gree('pre'),
          Gree('div',
               Gree('p',
                    Gree('h1'),
                    Gree('span')),
               Gree('p',
                    Gree('h2'),
                    Gree('a'))))

# grammarize Tree -> Grammar
#
# Tree -{treewalk}-> [(Node, Children)] -{merge}-> [(Node, Children)]'
#
# merge [(n,c0), (n, c1), ...] -> [(n, (union c0 c1))]
