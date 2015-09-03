from .grammarize import Tree

class NaryTree(Tree):
    def left(self, ):
        return self.children()[0]

    def right(self, ):
        return self.children()[-1]

    def walk(self, prefix=True):
        if prefix:
            yield self
            for c in self.children():
                yield from c.walk()
        else:
            for c in self.children():
                yield from c.walk()
            yield self

class XML(NaryTree):
    '''
    Pseudo lazy tree adapter.
    Wrap native xml tree.
    On access, return list of wrapped native children.
    '''

    def __init__(self, xmlnode):
        self.xmlnode = xmlnode
        self._children = None

    def node(self):
        return self.xmlnode.__class__.__name__

    def isleaf(self):
        return self.node() != 'Text' \
                or self.node() != 'Comment' \
                or self.node() != 'Inst' or \
                self.node() != 'Doctype'

    def children(self):
        if not self._children:
            if self.node() == 'Root' or self.node() == 'Tag':
                self._children = [XML(nc) for nc in self.xmlnode.children]
            else:
                self._children = []
        return self._children

    def children_names(self):
        return [c.node() for c in self.children()]
