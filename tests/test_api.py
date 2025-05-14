import json
import logging

from api_objects.shuffle_the_cards_obj import ShuffleTheCards, ShuffleTheCardsAssertion
import pytest
from utils.file_handler import *

test_data = [
    ['Shiffle the cards response schema check', 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1', 200],
    ['Shiffle the cards with 1 decks and check response success', 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1', 200],
    ['Shiffle the cards with 2 decks and check response success', 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=2', 200],
    ['Shiffle the cards with 20 decks and check response success', 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=20', 200],
    ['Shiffle the cards with 21 decks', 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=21', 200],
    ['Shiffle the cards with 0 deck', 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=0', 200],
    ['Shiffle the cards with -1 deck', 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=-1', 200],
    ['Shiffle the cards with "1" deck', 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count="1"', 500]]

@pytest.fixture(scope="function")
def prepare_params(setup, request):
    routed_path = f'deck/new/shuffle/?deck_count={request.param}'
    api_url = f'{setup.url_prefix}{routed_path}'
    setup.logic_controller = ShuffleTheCards(api_url, setup.dataset)
    yield setup


class TestAPI:

    @pytest.mark.parametrize("prepare_params", [1, 2, 20], indirect=True)
    def test_shuffle_card_positive(self, prepare_params, setup):
        logging.warning("in test warning")

        res = setup.logic_controller.shuffle_the_cards()
        ShuffleTheCardsAssertion.verify_shuffle_card_positive_schema(res)
        df = read_csv_dicts('/Users/michaelkuo/Codes/APIInterviewTemplate/data/shuffle_the_cards.csv')
        test_data = list()
        for column in df:
            li = list()
            li.append(column["Title"])
            li.append(column["Request"])
            li.append(column['Expected Response status'])
            test_data.append(li)

        print(test_data)
        pass