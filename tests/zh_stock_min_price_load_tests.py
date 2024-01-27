# -*-coding:utf-8 -*-
"""unit test for load stock price by minutes"""
import unittest

from notifications import zh_stock_price_big_change_warn as warn

class TestInternalMethods(unittest.TestCase):
    """ test internal methods """
    def test_whether_sent_today(self):
        """ test """
        self.assertEqual(warn.whether_sent_today("600000"), False)
        warn.update_sent_today("600000")
        self.assertEqual(warn.whether_sent_today("600000"), True)

if __name__ == '__main__':
    unittest.main()
