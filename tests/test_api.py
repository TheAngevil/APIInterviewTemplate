from api_objects.shuffle_the_cards_obj import ShuffleTheCards, ShuffleTheCardsAssertion
import pytest

limit_cases = [
    pytest.param(21, "The max number of Decks is 20.", id="too_many"),
    pytest.param(0,  "The min number of Decks is 1.",  id="zero"),
    pytest.param(-1, "The min number of Decks is 1.",  id="negative"),
]

limit_cases_error = [
    pytest.param(21, "The max number of Decks is 21.", id="too_many"),
    pytest.param(0,  "The min number of Decks is 2.",  id="zero"),
    pytest.param(-1, "The min number of Decks is 3.",  id="negative"),
]


@pytest.fixture(scope="function")
def prepare_params(setup, request):
    """
    To assemble the request
    :param setup:
    :param request:
    :return:
    """
    routed_path = f'deck/new/shuffle/?deck_count={request.param}'
    api_url = f'{setup.url_prefix}{routed_path}'
    setup.logic_controller = ShuffleTheCards(api_url, setup.dataset)
    yield setup

class TestAPI:
    @pytest.mark.parametrize("prepare_params", [1, 2, 20], indirect=True) # The number represents the number of decks
    def test_shuffle_card_positive(self, prepare_params, setup, request):
        """
        To test 1, 2, and 20 decks works normally on status code, response schema, and number of total cards
        """
        number_of_decks = request.node.callspec.params["prepare_params"]
        res = setup.logic_controller.shuffle_the_cards()
        ShuffleTheCardsAssertion.verify_shuffle_card_positive_status_code_200(res)
        ShuffleTheCardsAssertion.verify_shuffle_card_positive_response_schema(res)
        ShuffleTheCardsAssertion.verify_shuffle_card_positive_response_value(res, number_of_decks) # as number of decks

    @pytest.mark.parametrize("prepare_params", ["\"1\""], indirect=True)
    def test_shuffle_card_bad_parameter(self, prepare_params, setup):
        """
        To test "1" as an string is an invalid parameter and will have response status_code 500
        """
        res = setup.logic_controller.shuffle_the_cards()
        ShuffleTheCardsAssertion.verify_shuffle_card_negative_status_code_500(res)

    @pytest.mark.parametrize(("prepare_params", "expected_message"), limit_cases, indirect=["prepare_params"])
    def test_shuffle_card_exceed_deck_limitation(self, prepare_params, setup, expected_message):
        """
        Border test, to check 21, 0 or -1 decks will have have proper error messages in the response
        :param prepare_params:
        :param setup:
        :param expected_message:
        :return:
        """
        res = setup.logic_controller.shuffle_the_cards()
        ShuffleTheCardsAssertion.verify_shuffle_card_positive_status_code_200(res)
        ShuffleTheCardsAssertion.verify_shuffle_card_exceed_deck_limitation_scheme(res)
        ShuffleTheCardsAssertion.verify_shuffle_card_exceed_deck_limitation_value(res, expected_message)

    @pytest.mark.parametrize(("prepare_params", "expected_message"), limit_cases, indirect=["prepare_params"])
    def test_shuffle_card_exceed_deck_limitation_error(self, prepare_params, setup, expected_message):
        """
        Fail test to check assertion is correct
        :param prepare_params:
        :param setup:
        :param expected_message:
        :return:
        """
        res = setup.logic_controller.shuffle_the_cards()
        ShuffleTheCardsAssertion.verify_shuffle_card_negative_status_code_500(res)
        ShuffleTheCardsAssertion.verify_shuffle_card_exceed_deck_limitation_scheme(res)
        ShuffleTheCardsAssertion.verify_shuffle_card_exceed_deck_limitation_value(res, limit_cases_error)


