from utils.base_request import Base, BaseAssertion
import pytest
from pytest import assume
import logging

class ShuffleTheCards(Base):
    def __init__(self, url, data_set):
        Base.__init__(self)
        self.data_set = data_set
        self.url = url

    def shuffle_the_cards(self):
        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=self.url
        )
        return res


class ShuffleTheCardsAssertion(BaseAssertion):

    @classmethod
    def verify_shuffle_card_positive_status_code_200(cls, res: Base.ResponseObject):
        cls.verify_general_response_code_200(res)

    @classmethod
    def verify_shuffle_card_negative_status_code_500(cls, res: Base.ResponseObject):
        cls.verify_general_bad_request_with_500(res)

    @classmethod
    def verify_shuffle_card_positive_response_schema(cls, res: Base.ResponseObject):
        body = res.json
        with assume: assert (isinstance(body['success'], bool)), logging.error(
            'Expecting response "success" to be bool')
        with assume: assert (isinstance(body['shuffled'], bool)), logging.error(
            'Expecting response "shuffled" to be bool')
        with assume: assert (isinstance(body['remaining'], int)), logging.error(
            'Expecting response "remaining" to be int')
        with assume: assert (isinstance(body['deck_id'], str)), logging.error(
            'Expecting response "deck_id" to be str')
        with assume: assert (len(body['deck_id']) == 12), logging.error(
            'Expecting response "deck_id" to be 12')

    @classmethod
    def verify_shuffle_card_positive_response_value(cls, res: Base.ResponseObject, request_deck):
        body = res.json
        with assume: assert (body['success']), logging.error(
            'Expecting response "success" to be True')
        with assume: assert (body['shuffled']), logging.error(
            'Expecting response "shuffled" to be True')
        with assume: assert (body['remaining'] == 52*request_deck), logging.error(
            'Expecting response "remaining" to be int')


    @classmethod
    def verify_shuffle_card_exceed_deck_limitation_scheme(cls, res: Base.ResponseObject):
        body = res.json
        with assume: assert (isinstance(body['success'], bool)), logging.error(
            'Expecting response "success" to be bool')
        with assume: assert (isinstance(body['error'], str)), logging.error(
            'Expecting response "error" to be str')


    @classmethod
    def verify_shuffle_card_exceed_deck_limitation_value(cls, res: Base.ResponseObject, error_message):
        body = res.json
        with assume: assert (body['success'] == False), 'Expecting response "success" to be False'
        with assume: assert (body['error'] == error_message), 'Expecting response "error" to match error message'
