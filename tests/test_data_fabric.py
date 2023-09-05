import unittest
from requests import Response

from appian_locust._data_fabric import _DataFabric, DATA_FABRIC_URI_PATH
from appian_locust._interactor import _Interactor

integration_url = ""
auth = ["fake_user", ""]


class TestDataFabric(unittest.TestCase):

    def setUp(self) -> None:
        self.interactor: _Interactor = _Interactor("", "ase")
        setup_headers_mock = unittest.mock.Mock(return_value={})
        setattr(self.interactor, 'setup_sail_headers', setup_headers_mock)
        setattr(self.interactor, 'setup_request_headers', setup_headers_mock)
        self.data_fabric_interactor: _DataFabric = _DataFabric(self.interactor)

    def test_fetch_design_json(self) -> None:
        response_mock = unittest.mock.Mock(return_value={"ase": "ase2"})
        response_all_ok_mock = unittest.mock.Mock(return_value="")
        response = Response()
        setattr(response, 'json', response_mock)
        setattr(response, 'raise_for_status', response_all_ok_mock)  # ensure response.ok returns true
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == DATA_FABRIC_URI_PATH else "",
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        output = self.data_fabric_interactor.fetch_data_fabric_json()
        self.assertEqual(output, {"ase": "ase2"})
