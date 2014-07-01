import unittest

from ..utils import get_resource_type as grt
from . import eq_


class TestGetResourceType(unittest.TestCase):

    def test_other(self):
        eq_(grt('', ''), 'other')
        eq_(grt('', None), 'other')
        eq_(grt(None, ''), 'other')
        eq_(grt(None, None), 'other')

    def test_css(self):
        eq_(grt('text/css', 'style.css'), 'css')
        eq_(grt('TEXT/CSS', 'style.css'), 'css')
        eq_(grt('text/plain', 'style.css'), 'css')
        eq_(grt('text/plain', 'style.css?swag'), 'css')

        eq_(grt('text/css', 'xxx.xxx'), 'css')
        eq_(grt('xxx/xxx', 'style.css'), 'css')
        eq_(grt('text/plain', 'style.css'), 'css')

    def test_js(self):
        eq_(grt('application/javascript', 'yolo.js'), 'js')
        eq_(grt('text/plain', 'yolo.js'), 'js')
        eq_(grt('text/plain', 'yolo.js?swag=8675309'), 'js')
        eq_(grt('application/javascript', 'yolo.js?script'), 'js')

        eq_(grt('application/javascript', 'xxx.xxx'), 'js')
        eq_(grt('text/javascript', 'xxx.xxx'), 'js')
        eq_(grt('xxx/xxx', 'lol.js'), 'js')
        eq_(grt('xxx/xxx', 'lol.js?swag=8675309'), 'js')

    def test_json(self):
        eq_(grt('application/json; charset=utf-8', 'xxx.xxx'), 'json')
        eq_(grt('application/json', 'xxx.xxx'), 'json')
        eq_(grt('application/webapp-manifest+json', 'xxx.xxx'), 'json')
        eq_(grt('text/x-json', 'xxx.xxx'), 'json')
        eq_(grt('text/json', 'xxx.xxx'), 'json')
        eq_(grt('xxx/xxx', 'lol.json'), 'json')
        eq_(grt('xxx/xxx', 'lol.json?swag=8675309'), 'json')

    def test_xml(self):
        eq_(grt('application/xml', 'xxx.xxx'), 'xml')
        eq_(grt('text/xml', 'xxx.xxx'), 'xml')
        eq_(grt('xxx/xxx', 'lol.xml'), 'xml')

    def test_image(self):
        eq_(grt('image/gif', 'hyfr.gif'), 'image')
        eq_(grt('image/ief', 'yolo.gif'), 'image')
        eq_(grt('image/jpeg', 'mustard.gif'), 'image')
        eq_(grt('image/jpeg', 'DSC8675309.JPG'), 'image')

        eq_(grt('image/gif', 'xxx.xxx'), 'image')
        eq_(grt('xxx/xxx', 'lol.gif'), 'image')
        eq_(grt('text/plain', 'lol.gif'), 'image')

    def test_audio(self):
        eq_(grt('audio/mp3', 'xxx.xxx'), 'audio')
        eq_(grt('xxx/xxx', 'lol.mp3'), 'audio')

        eq_(grt('audio/ogg', 'xxx.xxx'), 'audio')
        eq_(grt('xxx/xxx', 'lol.ogg'), 'audio')

        eq_(grt('audio/wav', 'xxx.xxx'), 'audio')
        eq_(grt('xxx/xxx', 'lol.wav'), 'audio')

        eq_(grt('audio/weba', 'xxx.xxx'), 'audio')
        eq_(grt('xxx/xxx', 'lol.weba'), 'audio')

    def test_video(self):
        eq_(grt('video/flv', 'xxx.xxx'), 'video')
        eq_(grt('xxx/xxx', 'lol.flv'), 'video')

        eq_(grt('video/webm', 'xxx.xxx'), 'video')
        eq_(grt('xxx/xxx', 'lol.webm'), 'video')

        eq_(grt('video/mp4', 'xxx.xxx'), 'video')
        eq_(grt('xxx/xxx', 'lol.mp4'), 'video')

    def test_flash(self):
        eq_(grt('application/x-shockwave-flash', 'xxx.xxx'), 'flash')
        eq_(grt('xxx/xxx', 'lol.swf'), 'flash')

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

    def test_doc(self):
        eq_(grt('xxx/xxx', 'index.html'), 'doc')
        eq_(grt('xxx/xxx', 'index.htm'), 'doc')
        eq_(grt('xxx/xxx', 'index.HTM?swag'), 'doc')

        eq_(grt('text/plain', 'lol.txt'), 'doc')
        eq_(grt('text/plain', 'xxx.xxx'), 'doc')

        eq_(grt('text/html', 'lol.html'), 'doc')
        eq_(grt('text/html', 'xxx.xxx'), 'doc')

        eq_(grt('text/html; charset=utf-8', 'lol.html'), 'doc')
        eq_(grt('text/html; charset=utf-8', 'xxx.xxx'), 'doc')


if __name__ == '__main__':
    unittest.main()
