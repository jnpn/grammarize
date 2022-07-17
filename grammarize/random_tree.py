'''
Random Tree generator (depth bound) on top of grammarize.grammarize.
'''

from itertools import cycle

from grammarize.grammarize import Gree


class IRandomTree:
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

    def generate(self, d):
        pass


class RandomTree(IRandomTree):
    """
    Generate a ~random tree from built-in tag list self.tags.
    """

    def __init__(self):
        """
        Initializes built-in tag list.
        """
        super().__init__()
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
        if d > 0:
            dn = d - 1
            return Gree(t, self.generate(dn), self.generate(dn))

        return None
