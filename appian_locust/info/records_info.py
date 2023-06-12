from typing import Any, Dict

from .._locust_error_handler import log_locust_error
from .._records import _Records


class RecordsInfo():
    """
    Class which provides metadata about available record types from the Tempo Records tab
    """

    def __init__(self, records: _Records):
        self.__records = records

    def get_all_available_record_types(self, locust_request_label: str = "Records.MainMenu_ViewAll") -> Dict[str, Any]:
        """
        Get all metadata for visible record types on Tempo Records.

        Returns (dict): List of record types and associated metadata
        """
        try:
            self.__records.get_records_interface(locust_request_label=locust_request_label)
            self.__records.get_records_nav(locust_request_label=locust_request_label)
        except Exception as e:
            log_locust_error(e, error_desc="Response Error", raise_error=False)
        return self.__records.get_all_record_types(locust_request_label=locust_request_label)
