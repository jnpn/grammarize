from grammarize.grammarize import RandomTree

if __name__ == "__main__":

    print('Grammar inference')
    from tests.test_gree import t0, t1, t2, t3, g3
    for tree in [t0, t1, t2, t3, g3]:
        print('@Source')
        print(tree)
        print('@Grammar')
        print(tree.bnf())

    print('Random tree generation')

    tags = ["a", "pre", "div", "span",
            "h1", "h2", "h3", "code",
            "img", "audio", "video", "script"]

    count = 5                   # number of trees
    depth = 10                  # trees of depth <= 10
    trees = [RandomTree().generate(depth) for i in range(count)]
    for num, tree in enumerate(trees):
        print("Tree", num)
        print(tree.bnf())
