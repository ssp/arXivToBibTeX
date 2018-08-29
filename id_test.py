#!/usr/bin/env python

import unittest
from lookup import prepareArXivID
from lookup import extractPapersFromArXivUriPath

class TestIDMethods(unittest.TestCase):

    def test_ID(self):
        """ contains test cases [input, output]"""
        cases = [
            # new-style IDs
            ['1504.12345', '1504.12345'], # 5 digits per month
            ['150412345', '1504.12345'], # forgotten . separator
            ['0909.1234', '0909.1234'], # 4 digits per month
            # old-style IDs
            ['math/0606123', 'math/0606123'],
            ['hep-th/0606123', 'hep-th/0606123'],
            ['0606123', 'math/0606123'], # no prefix -> math
            ['hep-th/0606123', 'hep-th/0606123'],
            # strip trailing version number
            ['1504.12345v2', '1504.12345'],
            ['math/0606123v4', 'math/0606123'],
        ]

        for case in cases:
            self.assertEqual(
                prepareArXivID(case[0]),
                case[1]
            )

    def test_extractFromUri(self):
        """ contains test cases [input, output]"""
        cases = [
            ['https://arxiv.org/abs/1504.02345', '1504.02345'], # 5 digits per month
            ['https://arxiv.org/abs/quant-ph/0304179', 'quant-ph/0304179'] # issue 10
        ]

        for case in cases:
            self.assertEqual(
                extractPapersFromArXivUriPath(case[0]),
                case[1]
            )


if __name__ == '__main__':
    unittest.main()