from unittest import TestCase

import uuid

from com.goffersoft.myproj import uniqid

class TestUniqid(TestCase):
    def test_is_string(self):
        u = uniqid.get_uniqid()
        self.assertTrue(isinstance(u, uuid.UUID))
