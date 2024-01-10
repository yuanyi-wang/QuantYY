# -*-coding:utf-8 -*-

import unittest

import jobs.zh_stock_min_price_load as job

class TestInternalMethods(unittest.TestCase):


    def test_whether_sent_today(self):
        self.assertEqual(job._whether_sent_today("600000"), False)
        job._update_sent_today("600000")
        self.assertEqual(job._whether_sent_today("600000"), True)

if __name__ == '__main__':
    unittest.main()