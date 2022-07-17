'''
Grammarize

Implements grammatical rules inference from Tree -> Grammar
'''


from itertools import groupby

from .prelude import flatten, isnt


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

    def maybe(self, v, f, p, d):
        return f(v) if p(v) else d

    def mayli(self, v, f):
        return self.maybe(v, f, isnt(None), [])

    def children(self):
        listify = lambda e: [e]
        maybeleft = self.mayli(self.left(), listify)
        mayberight = self.mayli(self.right(), listify)
        return [] + maybeleft + mayberight

    def children_names(self):
        return [c.node() for c in self.children()]

    def __repr__(self):
        if self.isleaf():
            return '(Leaf %s)' % (self.node())
        else:
            return '(Tree %s %s %s)' % (self.node(), self.left(), self.right())

    def pp(self, prefix='-', indenter=' ', indentation=1, step=2):
        '''pretty printer'''
        print(prefix + indenter * indentation, self.__class__.__name__, self.node())
        if self.left():
            self.left().pp(indentation=indentation + step)
        if self.right():
            self.right().pp(indentation=indentation + step)

    def walk(self):
        """
        Tree -> [Tree]
        t (+) default walk left (+) default walk right
        """
        theres = isnt(None)
        if theres(self.left()):
            yield from self.left().walk()
        yield self
        if theres(self.right()):
            yield from self.right().walk()


class Gree(Tree):
    """
    Grammarize Tree -> Grammar

    Tree -{treewalk}-> [(Node, Children)] -{merge}-> [(Node, Children)]'

    merge [(n,c0), (n, c1), ...] -> [(n, (union c0 c1))]

    TODO:

      - order rules by depth of first appearance
    """

    def rules_(self):
        """tree -> [(parent, [childrens])]"""
        return [(t.node(), t.children_names())
                for t in self.walk()
                if not t.isleaf()]

    def rules__(self):
        def clean(l):
            """[(tag, [subtag])] -> Union [subtag]"""
            return set(flatten([s for e, s in l]))
        parent_name = lambda t: t[0]
        # @INFO: groupby is order sensitive
        # groupby a e b e != groupby a b e e
        # Tree.walk traversal order exposed
        # the need for sorting
        sr = sorted(self.rules_(), key=parent_name)
        return [(p, clean(cs)) for p, cs in groupby(sr, parent_name)]

    def rules(self):
        return dict(self.rules__())

    def bnf(self):
        """
        pretty prints grammar rules in BNF forms.
        """
        symbolify = lambda s: '<%s>' % s
        disjonctify = lambda l: ' | '.join(l)
        equalify = lambda a, b: " ::= ".join([a, b])
        nl = "\n"
        return nl.join([equalify(symbolify(p), disjonctify(map(symbolify, cs)))
                        for p, cs
                        in self.rules().items()])

class Grouper:

    def __init__(self):
        self.d = {}

    def add(self, k, v):
        if k in self.d:
            kset = self.d[k]
            # only add if new
            if v not in kset:
                kset.add(v)
        else:
            self.d[k] = set([v])

    def to_dict(self):
        return self.d

    def __repr__(self):
        '''dict[A,set(B)] -> str'''
        kvs = ', '.join(f'{k}:{s}' for k,s in self.d.items())
        return f'<Grouper {kvs}>'

class G(dict):

    '''Grouping dict key -> set(val).'''

    def __setitem__(self, k, v):
        if k in self:
            kset = self[k]
            if v not in kset:
                kset.add(v)
        else:
            print('debug', k, v)
            super().__setitem__(k, set([v]))
