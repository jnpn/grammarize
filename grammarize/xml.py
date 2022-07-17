'''
XML-like trees adapters.
'''

import re

from .grammarize import Gree, Tree


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

    Warning: XML NaryTrees don't have leaves, since unnecessary
    for grammar inference.
    '''

    def __init__(self, xmlnode):
        self.xmlnode = xmlnode

    def node(self):
        kind = self.xmlnode.__class__.__name__
        if kind == 'Root':
            return 'Document'
        else:
            def p(n):
                rx = r'<(?P<name>[^ ]+).*>'
                return re.match(rx, n).groups('name')[0]
            n = self.xmlnode.name
            return p(n) if isinstance(n, str) else p(n.decode('utf8').strip())

    def children(self):
        def is_xml_node(n):
            k = n.__class__.__name__
            return k in ['Root', 'Tag']
        return [XML(nc) for nc in self.xmlnode.children if is_xml_node(nc)]

    def children_names(self):
        return [c.node() for c in self.children()]

    def __repr__(self):
        return self.node()


class NaryGree(XML, Gree):

    def rules_(self):
        return [(t.node(), t.children_names())
                for t in self.walk()]
