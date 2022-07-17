from rich.console import Console
from rich.highlighter import RegexHighlighter


class ParensHighlighter(RegexHighlighter):
    base_style = "example."
    highlights = [r'(?P<lpar>[(]).*(?P<rpar>[)])']

class AssignHighlighter(RegexHighlighter):
    base_style = "example."
    highlights = [r'(?P<lval>.*) ?(?P<eq>::=)?(?P<rval>.*)']

class TagHighlighter(RegexHighlighter):
    base_style = "example."
    highlights = [r'(?P<openb>[<])(?P<tag>[^>]*)(?P<closeb>[>])']

#

class GreeHighlighter(RegexHighlighter):
    base_style = "example."
    highlights = [r' *(?P<kind>(Gree|Tree|Leaf)) (?P<tag>[^ )]+)']
