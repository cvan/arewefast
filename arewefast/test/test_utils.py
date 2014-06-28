import unittest

from ..utils import get_resource_type as grt
from . import eq_


class TestGetResourceType(unittest.TestCase):

    def test_css(self):
        eq_(grt('text/css', 'style.css'), 'css')
        eq_(grt('TEXT/CSS', 'style.css'), 'css')
        eq_(grt('text/plain', 'style.css'), 'css')
        eq_(grt('text/plain', 'style.css?swag'), 'css')

        eq_(grt('text/css', 'xxx.xxx'), 'css')
        eq_(grt('xxx/xxx', 'style.css'), 'css')
        eq_(grt('text/plain', 'style.css'), 'css')

    def test_image(self):
        eq_(grt('image/gif', 'hyfr.gif'), 'image')
        eq_(grt('image/ief', 'yolo.gif'), 'image')
        eq_(grt('image/jpeg', 'mustard.gif'), 'image')
        eq_(grt('image/jpeg', 'DSCLOLOL123.JPG'), 'image')

        eq_(grt('image/gif', 'xxx.xxx'), 'image')
        eq_(grt('xxx/xxx', 'lol.gif'), 'image')
        eq_(grt('text/plain', 'lol.gif'), 'image')

    def test_xml(self):
        eq_(grt('text/xml', 'xxx.xxx'), 'xml')
        eq_(grt('xxx/xxx', 'lol.xml'), 'xml')

    def test_audio(self):
        eq_(grt('audio/ogg', 'xxx.xxx'), 'audio')
        eq_(grt('xxx/xxx', 'lol.ogg'), 'audio')

    def test_font(self):
        # EOT
        eq_(grt('application/vnd.ms-fontobject', 'xxx.xxx'), 'font')
        eq_(grt('xxx/xxx', 'comicsans.eot#iefix'), 'font')

        # OTF
        eq_(grt('application/font-sfnt', 'xxx.xxx'), 'font')
        eq_(grt('font/otf', 'xxx.xxx'), 'font')
        eq_(grt('xxx/xxx', 'comicsans.otf'), 'font')

        # SVG
        # eq_(grt('image/svg+xml', 'comicsans.lol'), 'font')
        # eq_(grt('text/plain', 'comicsans.svg'), 'font')

        # TTF
        eq_(grt('application/font-sfnt', 'xxx.xxx'), 'font')
        eq_(grt('font/ttf', 'xxx.xxx'), 'font')
        eq_(grt('xxx/xxx', 'comicsans.ttf'), 'font')

        # WOFF
        eq_(grt('application/font-woff', 'comicsans.lol'), 'font')
        eq_(grt('font/x-woff', 'comicsans.lol'), 'font')
        eq_(grt('xxx/xxx', 'comicsans.woff'), 'font')


if __name__ == '__main__':
    unittest.main()
