'''
Grammarize

Implements grammatical rules inference from Tree -> Grammar
Also contains a random Tree generator (depth bound).
'''


from itertools import groupby, cycle
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
        symbolify = lambda s: '<%s>' % s
        disjonctify = lambda l: ' | '.join(l)
        equalify = lambda a, b: " ::= ".join([a, b])
        nl = "\n"
        # return {symbolify(p): disjonctify(map(symbolify,cs))
        #  for p,cs in self.rules().items()}
        return nl.join([equalify(symbolify(p), disjonctify(map(symbolify, cs)))
                        for p, cs
                        in self.rules().items()])


class IRandomTree(object):
    """Random tree generator, with some constraints.
         - T stream of tags, fixed iterable or generator
       ```
       if (d > 0):
         d' = d - 1
         gen(T, d) -> Tree(next T, gen T d', gen T d')
       else:
         gen(T, d) -> None
       ```

    TODO:

      - different way to pick tags (probabilities, markovian rules ...)
    """

    def __init__(self, depth=18):
        """

        Arguments:
        - `depth`: maximum depth of the generated tree
        """
        self._depth = depth

    def generate(self): pass


class RandomTree(IRandomTree):
    """
    Generate a ~random tree from built-in tag list self.tags.
    """

    def __init__(self, ):
        """
        Initializes built-in tag list.
        """
        super()
        self.tags = cycle(["a", "pre",
                           "div", "span",
                           "h1", "h2",
                           "h3", "code",
                           "img", "audio",
                           "video", "script"])

    def generate(self, d):
        """
        Simply depth bounded tree generation.
        """
        t = next(self.tags)
        if (d > 0):
            dn = d - 1
            return Gree(t, self.generate(dn), self.generate(dn))
        else:
            return None
