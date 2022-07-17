import unittest

from grammarize.grammarize import Gree


class TestGree(unittest.TestCase):

    def setUp(self):
        self.t0 = Gree("body",
                       Gree("div"),
                       Gree("div"))

        self.t1 = Gree("body",
                       Gree("div"),
                       Gree("div",
                            Gree("wat",
                                 Gree("duh"),
                                 Gree("eww"))))

        self.t2 = Gree("body",
                       Gree("ldiv"),
                       Gree("rdiv",
                            Gree("lwat",
                                 Gree("lduh"),
                                 Gree("leww")),
                            Gree("rwat",
                                 Gree("rduh"),
                                 Gree("reww")),
                            ),
                       )

        self.t3 = Gree("body",
                       Gree("pre"),
                       Gree("div",
                            Gree("p",
                                 Gree("h1"),
                                 Gree("span")),
                            Gree("p",
                                 Gree("h2"),
                                 Gree("a")),
                            ),
                       )

        self.g3 = Gree("body",
                       Gree("pre"),
                       Gree("div",
                            Gree("p",
                                 Gree("h1"),
                                 Gree("span")),
                            Gree("p",
                                 Gree("h2"),
                                 Gree("a")),
                            ),
                       )

    def test_0(self):
        l = Gree("div")
        r = Gree("div")
        t = Gree("body", l, r)
        value = list(self.t0.walk())
        expected = [l, t, r]
        self.assertEqual(value, expected)

    def test_1(self):
        l = Gree("div")
        r = Gree("div")
        t = Gree("html", l, r)
        value = list(self.t0.walk())
        expected = [l, t, r]
        self.assertNotEqual(value, expected)
