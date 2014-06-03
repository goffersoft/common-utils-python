from unittest import TestCase

from com.goffersoft.myproj import hello


class TestHello(TestCase):
    def test_is_string(self):
        s = hello.say_hello()
        self.assertTrue(isinstance(s, basestring))
