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

def flatten(l):
    """
    case x:xs of
     atom x -> 
     list x -> 
     _      -> 
    """

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

def Tree(v,l=None,r=None):
    return (v, l, r)

# def Tree(v,l=None,r=None):
#     return [v, l, r]

def Leaf(v):
    return Tree(v)

def TreeNode(t):
    return t[0]

def TreeLeft(t):
    return t[1]

def TreeRight(t):
    return t[2]

def TreeIsLeaf(t):
    return TreeLeft(t) is None and TreeRight(t) is None

def TreeChildren(t):
    return [TreeLeft(t), TreeRight(t)]

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


def TreeWalk(t):
    """Tree -> [Tree]
    TOFIX: fails on non binary trees
    """
    # case leaf -> [Tree]
    if TreeIsLeaf(t):
        return [t]
    # case tree -> [Tree]
    else:
        # t (+) walk left (+) walk righto
        return [t] + TreeWalk(TreeLeft(t)) + TreeWalk(TreeRight(t))

        # Old dead code
        # 
        # r = [t]
        # r.append(TreeWalk(TreeLeft(t)))
        # r.append(TreeWalk(TreeRight(t)))
        # return r


def wrappend(l,v):
    c = l.copy()
    c.append(v)
    return c
    
# def TreeChildrenNames(tree):
#     if TreeIsLeaf(tree):
#         return None
#     else:
#         children = TreeChildren(tree)
#         nodename = lambda t: TreeNode(t)
#         return list(map(nodename, children))

def TreeRules_(tree):
    return list((TreeNode(t),TreeChildrenNames(t))
                for t in TreeWalk(tree)
                if not TreeIsLeaf(t))

# from collection import Counter

from functools import reduce
from itertools import groupby

# def inmap(l,e):
#     """group l elems by key extracted using function e"""
#     m = {}
#     return reduce(lambda a,b: a[e(b)['key']].append(e(b)['val']), l)

def TreeRules__(tree):
    # clean: [(tag, [subtag])] -> Union [subtag]
    def clean(l):
        return set(flatten([s for e,s in l]))
    return list((p, clean(cs)) for p,cs in groupby(TreeRules_(tree), TreeNode))

def TreeRules(tree):
    return dict(TreeRules__(tree))

# grammarize Tree -> Grammar
#
# Tree -{treewalk}-> [(Node, Children)] -{merge}-> [(Node, Children)]'
#
# merge [(n,c0), (n, c1), ...] -> [(n, (union c0 c1))]

def wat(tree):
    """ tree -> [(node, children)]"""
    def children(tree):
        return TreeChildren(tree)
    return flatmap(children, tree)
