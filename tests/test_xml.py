from nose.tools import assert_equal

from grammarize.xml import NaryGree

from sax.tokenizer.loop import tok as root
from sax.parser.core import pp, xml as xmlb


def test0():
    t = xmlb(root(open('./samples/cv.settings.xml', 'r')))
    pp(t)
    ng = NaryGree(t)
    print(ng.bnf())
    r = ng.rules()
    e = {'office:settings': {'config:config-item-set'},
         'office:document-settings': {'office:settings'},
         'config:config-item-map-indexed': {'config:config-item-map-entry'},
         'Document': {'office:document-settings'},
         'config:config-item-set': {'config:config-item-map-indexed',
                                    'config:config-item'},
         'config:config-item-map-entry': {'config:config-item'},
         'config:config-item': set()}
    assert_equal(r, e)
