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
    """
    ShuffleTheCards API specific assertions
    """
    @classmethod
    def verify_shuffle_card_positive_status_code_200(cls, res: Base.ResponseObject):
        cls.verify_general_response_code_200(res)

    @classmethod
    def verify_shuffle_card_negative_status_code_500(cls, res: Base.ResponseObject):
        cls.verify_general_bad_request_with_500(res)

    @classmethod
    def verify_shuffle_card_positive_response_schema(cls, res: Base.ResponseObject):
        body = res.json
        if not pytest.assume(isinstance(body['success'], bool)):
            logging.error('Expecting response "success" to be bool')
        if not pytest.assume(isinstance(body['shuffled'], bool)):
            logging.warning('Expecting response "shuffled" to be bool')
        if not pytest.assume(isinstance(body['remaining'], int)):
            logging.warning(
                'Expecting response "remaining" to be int')
        if not pytest.assume(isinstance(body['deck_id'], str)):
            logging.warning(
                'Expecting response "deck_id" to be str')
        if not pytest.assume(len(body['deck_id']) == 12):
            logging.warning(
                'Expecting response "deck_id" to be 12')


    @classmethod
    def verify_shuffle_card_positive_response_value(cls, res: Base.ResponseObject, request_deck):
        body = res.json
        if not pytest.assume(body['success']):
            logging.warning('Expecting response "success" to be True', stacklevel=2)

        if not pytest.assume(body['shuffled']):
            logging.warning('Expecting response "shuffled" to be True', stacklevel=2)

        if not pytest.assume(body['remaining'] == 52*request_deck):
            logging.warning('Expecting response "remaining" to be int', stacklevel=2)


    @classmethod
    def verify_shuffle_card_exceed_deck_limitation_scheme(cls, res: Base.ResponseObject):
        body = res.json
        if not pytest.assume(isinstance(body['success'], bool)):
            logging.warning('Expecting response "success" to be bool', stacklevel=2)
        if not pytest.assume(isinstance(body['error'], str)):
            logging.warning('Expecting response "error" to be str', stacklevel=2)

    @classmethod
    def verify_shuffle_card_exceed_deck_limitation_value(cls, res: Base.ResponseObject, error_message):
        body = res.json
        if not pytest.assume(body['success'] == False):
            logging.error(f'Expecting response "success": {body['success']} to be False', stacklevel=2)
        if not pytest.assume(body['error'] == error_message):
            logging.error(f'Expecting response "error": {body['error']} to match error message: {error_message}', stacklevel=2)

