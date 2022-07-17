from grammarize.grammarize import Gree
from grammarize.random_tree import RandomTree

def old():

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
        print(tree)
        print('@Grammar')
        print(tree.bnf())

    print()
    print('Random tree generation')
    print('----')

    tags = ["a", "pre", "div", "span",
            "h1", "h2", "h3", "code",
            "img", "audio", "video", "script"]

    count = 1                   # number of trees
    depth = 12                  # trees of depth <= 10
    trees = [RandomTree().generate(depth) for i in range(count)]
    for num, tree in enumerate(trees):
        print("Tree", num)
        print(tree.bnf())

if __name__ == "__main__":
    main()
