#!/usr/bin/env python

from itertools import groupby
from prelude import flatten, isnt

class Tree:
    """
    tree a -> (value a, left tree, right tree)
    t = (1 (2 None None) None)
    """

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

    def maybe(self,v,f,p,d):
        return f(v) if p(v) else d

    def mayli(self,v,f):
        return self.maybe(v, f, isnt(None), [])

    def children(self):
        listify    = lambda e: [e]
        maybeleft  = self.mayli(self.left(), listify)
        mayberight = self.mayli(self.right(), listify)
        return [] + maybeleft + mayberight

    def children_names(self):
        return [c.node() for c in self.children()]

    def __repr__(self):
        if self.isleaf():
            return '(Leaf %s)' % (self.node())
        else:
            return '(Tree %s %s %s)' % (self.node(), 
                                        self.left() if self.left() is not None else "", 
                                        self.right() if self.right() is not None else "")
    
    def walk(self):
        """
        Tree -> [Tree]
        t (+) default walk left (+) default walk right
        """

        walkify    = lambda e: e.walk()
        maywalk    = lambda s: self.mayli(s, walkify)
        return [self] + maywalk(self.left()) + maywalk(self.right())

class Gree(Tree):
    """
    Grammarize Tree -> Grammar
    
    Tree -{treewalk}-> [(Node, Children)] -{merge}-> [(Node, Children)]'
    
    merge [(n,c0), (n, c1), ...] -> [(n, (union c0 c1))]
    """

    def rules_(self):
        return [(t.node(),t.children_names()) for t in self.walk() if not t.isleaf()]

    def rules__(self):
        def clean(l):
            """[(tag, [subtag])] -> Union [subtag]"""
            return set(flatten([s for e,s in l]))
        parent_name = lambda t: t[0]
        return [(p, clean(cs)) for p,cs in groupby(self.rules_(), parent_name)]

    def rules(self):
        return dict(self.rules__())

    def bnf(self):
        symbolify   = lambda    s: '<%s>' % s
        disjonctify = lambda    l: ' | '.join(l)
        equallify   = lambda a, b: " ::= ".join([a,b])
        nl          = "\n"
        # return {symbolify(p): disjonctify(map(symbolify,cs)) for p,cs in self.rules().items()}
        return nl.join([equallify(symbolify(p),disjonctify(map(symbolify,cs)))
                        for p,cs
                        in self.rules().items()])

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

### Main

if __name__ == "__main__":
    from pprint import pprint as pp
    for tree in [t0,t1,t2,t3,g3]:
        print('@Source')
        print(tree)
        print('@Grammar')
        print(tree.bnf())
