'''
Grammarize CLI
'''

import click
import rich.pretty as pp

from grammarize.grammarize import Gree
from grammarize.random_tree import RandomTree
from grammarize.highlighters import ParensHighlighter, \
    TagHighlighter, AssignHighlighter, GreeHighlighter

from rich.console import Console
from rich.theme import Theme

@click.group('cli')
def cli():
    pass

theme = Theme({
    "example.rpar": "bold magenta",
    "example.lpar": "bold magenta",
    "example.eq": "bold cyan",
    "example.tag": "bold yellow",
    "example.kind": "bold blue",
    "example.lval": "bold green",
    "example.rval": "bold green",
})

parcons = Console(highlighter=ParensHighlighter(), theme=theme)
eqcons = Console(highlighter=AssignHighlighter(), theme=theme)
tagcons = Console(highlighter=TagHighlighter(), theme=theme)
greecons = Console(highlighter=GreeHighlighter(), theme=theme)

@cli.command()
@click.argument('depth', default=4, type=int)
def gen_tree(depth):
    tree = RandomTree().generate(depth)
    tree.pp()

@cli.command()
@click.argument('depth', default=4, type=int)
def show_bnf(depth):
    tree = RandomTree().generate(depth)
    grammar = tree.bnf()
    print()
    tree.pp()
    print()
    eqcons.print(grammar)

@cli.command()
def demo():

    print()
    print('Grammar inference')
    print('----')
    # commented because I don't understand python import system properly
    # from tests.test_gree import t0, t1, t2, t3, g3
    # for tree in [t0, t1, t2, t3, g3]:
    t = Gree('body',
          Gree('pre'),
          Gree('div',
               Gree('p',
                    Gree('h1'),
                    Gree('span')),
               Gree('p',
                    Gree('h2'),
                    Gree('a'))))
    for tree in [t]:
        print('@Source')
        greecons.print(tree)
        print('@Grammar')
        print(tree.bnf())

    print()
    print('Random tree generation')
    print('----')

    count = 1                   # number of trees
    depth = 12                  # trees of depth <= 10
    trees = [RandomTree().generate(depth) for i in range(count)]
    for num, tree in enumerate(trees):
        print("Tree", num)
        print(tree.bnf())

if __name__ == "__main__":
    parcons.print("Send funds to (johan.ponin.pro@gmail.com)")
    cli()
