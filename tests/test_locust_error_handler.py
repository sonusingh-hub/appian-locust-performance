import unittest

import locust
from appian_locust._locust_error_handler import (
    log_locust_error,
    trigger_request_event_for_error,
    INTERNAL_ERROR_RESPONSE,
)
from appian_locust.utilities.helper import ENV
from locust import events
from unittest.mock import Mock
from requests.models import Response, Request


class TestLocustErrorHandler(unittest.TestCase):

    def test_obtain_correct_location(self) -> None:
        ENV.stats.errors.clear()

        def run_with_error() -> None:
            e = Exception("abc")
            log_locust_error('label', e, raise_error=False)
        run_with_error()

        self.assertEqual(1, len(ENV.stats.errors))

        # Assert error structure
        error: locust.stats.StatsError = list(ENV.stats.errors.values())[0]
        self.assertEqual('DESC: No description', error.method)
        self.assertEqual('LOCATION: test_locust_error_handler.py/run_with_error()', error.name)
        self.assertEqual('EXCEPTION: abc', error.error)
        self.assertEqual(1, error.occurrences)

    def test_trigger_request_event_for_error(self) -> None:
        spy = Mock()
        @events.request.add_listener
        def spy_on_requests(
            request_type: str,
            name: str,
            response_time: int,
            response_length: int,
            response: Response,
            context: str,
            exception: Exception,
        ) -> None:
            spy(response.reason)
        trigger_request_event_for_error(
            'name',
            Exception('error'),
            resp=INTERNAL_ERROR_RESPONSE,
        )
        spy.assert_called_once_with('Internal System Error')


if __name__ == '__main__':
    unittest.main()
