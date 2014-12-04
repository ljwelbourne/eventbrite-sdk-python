#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

from eventbrite.models import Payload

from requests.structures import CaseInsensitiveDict

from .base import unittest, mock


class TestPayload(unittest.TestCase):

    def setUp(self):
        self.response = mock.Mock()
        self.response.json = lambda: {u'id': u'1234567890', u'first_name': u'Daniel', u'last_name': u'Greenfeld', u'emails': [{u'verified': True, u'email': u'danny@eventbrite.com', u'primary': True}], u'name': u'Daniel Greenfeld'}
        self.response.url = "https://www.eventbriteapi.com/v3/users/me/"
        self.response.ok = True
        self.response.elapsed = timedelta(5)
        self.response.headers = CaseInsensitiveDict()
        self.response.reason = u"OK"
        self.response.status_code = 200

        self.payload = Payload.create(self.response)

    def test_attributes(self):
        self.assertEqual(
            sorted([u'id', u'first_name', u'last_name', u'emails', u'name']),
            sorted(self.payload.keys())
        )
        self.assertEqual(
            self.payload.url,
            self.response.url
        )
        self.assertTrue(self.payload.ok)
        self.assertTrue(isinstance(self.payload.elapsed, timedelta))
        self.assertTrue(isinstance(self.payload.headers, CaseInsensitiveDict))

    def test_pretty(self):

        self.assertEqual(
            self.payload.pretty,
            "{u'emails': [{u'email': u'danny@eventbrite.com',\n              u'primary': True,\n              u'verified': True}],\n u'first_name': u'Daniel',\n u'id': u'1234567890',\n u'last_name': u'Greenfeld',\n u'name': u'Daniel Greenfeld'}"
        )


if __name__ == '__main__':
    unittest.main()
