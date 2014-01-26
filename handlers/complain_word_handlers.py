__author__ = 'ivan'

import json

from google.appengine.ext import db
from google.appengine.api import users

from objects.complained_word import ComplainedWord
from environment import JINJA_ENVIRONMENT
import constants.constants
from objects.global_dictionary_word import GlobalDictionaryWord
from base_handlers.admin_request_handler import AdminRequestHandler
from base_handlers.api_request_handlers import APIRequestHandler


class ComplainWordHandler(APIRequestHandler):
    def __init__(self, *args, **kwargs):
        super(ComplainWordHandler, self).__init__(*args, **kwargs)

    def post(self, *args, **kwargs):
        super(ComplainWordHandler, self).get_device_id(**kwargs)
        complained_word_json_list = \
            json.loads(self.request.get(constants.constants.get_title))
        for current_word_json in complained_word_json_list:
            current_word = ComplainedWord(device_id=self.device_id,
                                          word=current_word_json[constants.constants.complained_word],
                                          reason=current_word_json[constants.constants.reason])
            if constants.constants.word_to_replace in current_word_json:
                current_word.replacement_word = \
                    current_word_json[constants.constants.word_to_replace]
            current_word.put()


class ShowComplainedWords(AdminRequestHandler):
    def __init__(self, *args, **kwargs):
        super(ShowComplainedWords, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        template = JINJA_ENVIRONMENT.get_template('templates/complained_words.html')
        cnt = 0
        render_data = {constants.constants.render_data_name: []}
        for word in ComplainedWord.all():
            word_render = word
            word_render.cnt = cnt
            if word.replacement_word is None:
                word_render.replacement_word = ''
            render_data[constants.constants.render_data_name].append(word_render)
            cnt += 1

        render_data["quantity"] = len(render_data[constants.constants.render_data_name])
        if users.get_current_user():
            render_data["logout_link"] = users.create_logout_url('/')
        self.response.write(template.render(render_data))


class DeleteComplainedWords(AdminRequestHandler):
    def __init__(self, *args, **kwargs):
        super(DeleteComplainedWords, self).__init__(*args, **kwargs)

    def post(self, *args, **kwargs):
        for word in ComplainedWord.all():
            db.delete(word)
        self.redirect(constants.constants.show_complained_url)


class DeleteComplainedWord(AdminRequestHandler):
    def __init__(self, *args, **kwargs):
        super(DeleteComplainedWord, self).__init__(*args, **kwargs)

    def post(self, *args, **kwargs):
        deleted_word = self.request.get(constants.constants.deleted_word_name)
        for word in ComplainedWord.all():
            if word.word == deleted_word:
                db.delete(word)
        self.redirect(constants.constants.show_complained_url)


class DeleteFromGlobalDictionaryHandler(AdminRequestHandler):
    def __init__(self, *args, **kwargs):
        super(DeleteFromGlobalDictionaryHandler, self).__init__(*args, **kwargs)

    def post(self, *args, **kwargs):
        data = self.request.get(constants.constants.complained_word)
        word = GlobalDictionaryWord.get_by_key_name(data)
        if word is not None:
            if word.tags.find("-deleted") != -1:
                word.tags += "-deleted"
            word.put()
        for word in ComplainedWord.all():
            if word.word == data:
                db.delete(word)
        self.redirect(constants.constants.show_complained_url)



