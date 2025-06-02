from enum import Enum
import logging
from logging import config
import uuid
import requests
from requests.models import Response
import pytest

logger = logging.getLogger(__name__)


class Base(object):

    class TestLogger:
        @staticmethod
        def logging():
            warning = "This is the warning message"
            critical = "This is the critical message!"
            logger.info("info")
            logger.warning('Warning: %s', warning)
            logger.critical('Critical: %s', critical)


    class ResponseObject(object):
        """
        Process response
        """
        def __init__(self, response: Response):
            self.status_code = response.status_code
            self.content = response.content
            self.text = response.text
            try:
                self.json = response.json()
            except Exception as e:
                self.json = None
                if self.status_code != 500:
                    logger.warning(e, exc_info=True)
            self.header = response.headers
            self.url = response.url

    class RequestMethod(str, Enum):
        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"
        PATCH = "PATCH"

    def __init__(self) -> None:
        pass

    @staticmethod
    def gen_unique_str():
        id = uuid.uuid4()
        return id

    def send_request(self,
                     method: RequestMethod = RequestMethod.GET,
                     payload=None,
                     chunk_size: int = 0,
                     cookies=None,
                     custom_url: str = None,
                     headers=None,
                     files: list = None
                     ) -> ResponseObject:
        """
        construct API request
        :param method:
        :param payload:
        :param chunk_size:
        :param cookies:
        :param custom_url:
        :param headers:
        :param files:
        :return:
        """
        _payload = None

        if files: # to ensure _payload is a dictionary when file uploads are included, avoiding potential errors when constructing multipart/form-data requests.
            _payload = {}

        if custom_url is None:
            logger.warning("should provide url when sending request")

        if payload is None:
            if method != self.RequestMethod.GET:
                logger.warning("should provide payload when sending request")
        else:
            _payload = payload

        if headers is None:
            _headers = {"Content-Type": "application/json"}
        else:
            _headers = headers

        # new request session
        session_res = requests.session()

        match method:
            case self.RequestMethod.GET:
                res = session_res.get(custom_url, headers=_headers, cookies=cookies, stream=True)
            case self.RequestMethod.POST:
                res = session_res.post(custom_url, headers=_headers, cookies=cookies, stream=True, json=_payload, files=files)
            case self.RequestMethod.PUT:
                res = session_res.put(custom_url, headers=_headers, cookies=cookies, stream=True, json=_payload, files=files)
            case self.RequestMethod.DELETE:
                res = session_res.delete(custom_url, headers=_headers, cookies=cookies, stream=True)
            case  self.RequestMethod.PATCH:
                res = session_res.patch(custom_url, headers=_headers, cookies=cookies, stream=True, json=_payload, files=files)
            case _:
                res = session_res.get(custom_url, headers=_headers, cookies=cookies, stream=True)

        res_obj = self.ResponseObject(res)

        # Formalize output logs for all API tests
        logger.info("\n=============URL=================\n")
        logger.info(res_obj.url)
        logger.info("\n============Payload==============\n")
        logger.info(payload)
        logger.info("\n============Response=============\n")
        if len(res.content) < 10000:
            logger.info(res_obj.text)
        else:
            logger.info("Too large response body, skipped to print.")
        logger.info("\n=================================\n")

        return res_obj


class BaseAssertion:
    """
    Base assertion Class
    """

    @classmethod
    def log_assert(cls, func, messages):
        if not func:
            logging.error(messages)
        assert func, messages
        if not pytest.assume(func):
            logger.error(messages, stacklevel=4)

    @classmethod
    def verify_general_response_code_200(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 200, "Assertion Failure, The status code is not 200, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_response_code_with_201(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 201,
                       "Assertion Failure, The status code is not 201, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_response_code_with_202(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 202, "Assertion Failure, The status code is not 202, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_response_code_with_204(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 204,
                       "Assertion Failure, The status code is not 204, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_general_forbidden_response_code(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 403,
                       "Assertion Failure, The status code is not 403, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_response_code_with_404(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 404,
                       "Assertion Failure, The status code is not 404, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_general_bad_request(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 400,
                       "Assertion Failure, The status code is not 400, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_general_bad_request_with_403(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 403,
                       "Assertion Failure, The status code is not 403, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_general_bad_request_with_405(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 405,
                       "Assertion Failure, The status code is not 405, res.status code: {}".format(res.status_code))

    @classmethod
    def verify_general_bad_request_with_500(cls, res: Base.ResponseObject):
        cls.log_assert(res.status_code == 500,
                       "Assertion Failure, The status code is not 500, res.status code: {}".format(res.status_code))
