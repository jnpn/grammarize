'''
Grammarize

Implements grammatical rules inference from Tree -> Grammar
'''


from .prelude import isnt, listify, mayli


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

    def children(self):
        maybeleft = mayli(self.left(), listify)
        mayberight = mayli(self.right(), listify)
        return [] + maybeleft + mayberight

    def children_names(self):
        return [c.node() for c in self.children()]

    def __repr__(self):
        if self.isleaf():
            return f'(Leaf {self.node()})'
        return f'(Tree {self.node()} {self.left()} {self.right()})'

    def __eq__(self, other):
        return self.node() == other.node() \
            and self.left() == other.left() \
            and self.right() == other.right()

    def pp(self, prefix='-', indenter=' ', indentation=1, step=2):
        '''pretty printer'''
        indent = prefix + indenter * indentation
        print(indent, self.__class__.__name__, self.node())
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

    def rules(self):
        g = G()
        for t in self.walk():
            if not t.isleaf():
                for c in t.children_names():
                    g[t.node()] = c
        return g

    def bnf(self):
        """
        pretty prints grammar rules in BNF forms.
        """
        nl = "\n"
        disjonctify = ' | '.join
        return nl.join([f'<{p}>' + " ::= " + disjonctify(f'<{c}>' for c in cs)
                        for p, cs
                        in self.rules().items()])


class G(dict):
    '''
    Grouping dict key -> set(val).
    '''

    def __setitem__(self, k, v):
        if k in self:
            kset = self[k]
            if v not in kset:
                kset.add(v)
        else:
            super().__setitem__(k, set([v]))
