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
    def verify_shuffle_card_positive_schema(cls, res: Base.ResponseObject):

        body = res.json
        cls.verify_general_response_code_200(res)
        with assume: assert (isinstance(body['success'], str)), logging.error('The status code is not expedted')
