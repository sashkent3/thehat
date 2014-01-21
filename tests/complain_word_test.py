__author__ = 'ivan'
import json

import webapp2
from google.appengine.ext import testbed
import unittest2

from objects.complained_word import ComplainedWord
import main
import constants.constants


class complain_word_test(unittest2.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()

    def test_post(self):
        word1 = {constants.constants.complained_word: "vasya",
                 constants.constants.reason: "typo",
                 constants.constants.word_to_replace: "petya"}
        word2 = {constants.constants.complained_word: "vasya",
                 constants.constants.reason: "not_a_noun"}
        len_before = ComplainedWord.all().count()
        request = webapp2.Request.blank('/abc/complain')
        request.body = "json={0}". \
            format(json.dumps([word1, word2]))
        request.method = 'POST'
        request.get_response(main.app)
        response = request.get_response(main.app) # It is need to call it twice
        len_after = ComplainedWord.all().count()
        self.assertEqual(response.status_int, 200)
        self.assertEqual(len_after, len_before + 4)

    def test_get_table(self):
        word1 = {constants.constants.complained_word: "vasya",
                 constants.constants.reason: "typo",
                 constants.constants.word_to_replace: "petya"}
        word2 = {constants.constants.complained_word: "vasya",
                 constants.constants.reason: "not_a_noun"}
        request = webapp2.Request.blank('/abc/complain')
        request.body = "json={0}". \
            format(json.dumps([word1, word2]))
        request.method = 'POST'
        request.get_response(main.app)
        request = webapp2.Request.blank(
            constants.constants.show_complained_url)
        request.method = 'GET'
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 302)

    def test_erase(self):
        word1 = {constants.constants.complained_word: "vasya",
                 constants.constants.reason: "typo",
                 constants.constants.word_to_replace: "petya"}
        word2 = {constants.constants.complained_word: "kokoko",
                 constants.constants.reason: "not_a_noun"}
        request = webapp2.Request.blank('/abc/complain')
        request.body = "json={0}". \
            format(json.dumps([word1, word2]))
        request.method = 'POST'
        request.get_response(main.app)
        request.get_response(main.app)

        request = webapp2.Request.blank(
            constants.constants.delete_current_url)
        request.method = 'POST'
        request.body = "word=vasya"
        len_before = ComplainedWord.all().count()
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200) # not 200, because redirrect
        len_after = ComplainedWord.all().count()
        self.assertEqual(len_before, len_after)
        request = webapp2.Request.blank(
            constants.constants.delete_all_url)
        request.method = 'POST'
        response = request.get_response(main.app)
        self.assertEqual(ComplainedWord.all().count(), 4)


    def tearDown(self):
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest2.main()