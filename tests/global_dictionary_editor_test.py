__author__ = 'ivan'

import unittest2

from google.appengine.ext import testbed

from tests.base_functions import *
import main


class GlobalDictionaryEditorTest(unittest2.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.taskqueue_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
        self.testbed.init_user_stub()

    def tearDown(self):
        self.testbed.deactivate()


    @staticmethod
    def get_table(body):
        left, right = body.find("<tbody>"), body.find("</tbody>") + 8
        return body[left:right]


    @staticmethod
    def push_words(data, admin):
        request = make_request("/json_updater", "POST", admin, data)
        return request.get_response(main.app)

    @unittest2.expectedFailure
    def test_get_no_data(self):
        request = make_request("/admin/global_dictionary/edit/0", "GET")
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 302)
        setCurrentUser('usermail@gmail.com', '1', True)
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)
        table = GlobalDictionaryEditorTest.get_table(response.body)
        self.assertEqual(table.count("tr") / 2, 0)

    @unittest2.expectedFailure
    def test_get(self):
        GlobalDictionaryEditorTest.push_words("data=ff%0D%0Afff", True)
        GlobalDictionaryEditorTest.push_words("data=ff%0D%0Afff", True)

        request = make_request("/admin/global_dictionary/edit/0", "GET", True)
        response = request.get_response(main.app)
        table = GlobalDictionaryEditorTest.get_table(response.body)
        self.assertEqual(table.count("tr") / 2, 2)

    @unittest2.expectedFailure
    def test_get_2_lists(self):
        for i in range(80):
            GlobalDictionaryEditorTest.push_words("data={0}%0D%0A{1}%0D%0A{2}".format(i, str(i) + "d",
                                                                                      str(i) + 'dd'), True)

        request = make_request("/admin/global_dictionary/edit/0", "GET", True)
        response = request.get_response(main.app)
        table = GlobalDictionaryEditorTest.get_table(response.body)
        self.assertEqual(table.count("tr") / 2, 200)

        request = make_request("/admin/global_dictionary/edit/1", "GET", True)
        response = request.get_response(main.app)
        table = GlobalDictionaryEditorTest.get_table(response.body)
        self.assertEqual(table.count("tr") / 2, 40)

    @unittest2.expectedFailure
    def test_delete_admin(self):
        GlobalDictionaryEditorTest.push_words("data=ff%0D%0Afff", True)
        make_request("/admin/global_dictionary/delete", "POST", True, "word=ff").get_response(main.app)

        request = make_request("/admin/global_dictionary/edit/0", "GET", True)
        response = request.get_response(main.app)
        table = GlobalDictionaryEditorTest.get_table(response.body)
        self.assertEqual(table.count("tr") / 2, 1)

    @unittest2.expectedFailure
    def test_delete_no_admin(self):
        GlobalDictionaryEditorTest.push_words("data=ff%0D%0Afff", True)
        make_request("/admin/global_dictionary/delete", "POST", False, "word=ff").get_response(main.app)

        request = make_request("/admin/global_dictionary/edit/0", "GET", True)
        response = request.get_response(main.app)
        table = GlobalDictionaryEditorTest.get_table(response.body)
        self.assertEqual(table.count("tr") / 2, 2)









