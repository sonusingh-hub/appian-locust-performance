from typing import Any, Dict
from urllib.parse import quote

from ._interactor import _Interactor
from .records_helper import get_all_records_from_json
from .uiform import SailUiForm


class RecordListUiForm(SailUiForm):

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "RecordListUi"):
        super().__init__(interactor, state, breadcrumb)

    def filter_records_using_searchbox(self, search_term: str = "", locust_request_label: str = "") -> 'RecordListUiForm':
        """
        This method allows you to Filter the Record Type List (displaying record instance for a specific record type)
        which makes the same request when typing something in the search box and reloading the page.
        More interactions (with the filtered list) can be performed on the returned SailUiForm Object.

        Note: This is different from how an end user interacts with the SearchBox. In that case you would type something in the box
        and when you would unfocus from the box a reevaluation happens and then you click the 'Search' button which returns the filtered
        results.

        Examples:

            >>> form.filter_records_using_searchbox('Donuts')

        Returns (RecordListUiForm): The record type list UiForm with the filtered results.
        """
        context_label = locust_request_label or f"{self.breadcrumb}.RecordType.SearchByText"
        search_uri = f"{self.form_url}?searchTerm={quote(search_term)}"

        headers = self._interactor.setup_sail_headers()
        response = self._interactor.get_page(uri=search_uri, headers=headers, label=context_label)
        return RecordListUiForm(self._interactor, response.json(), breadcrumb=context_label)

    def get_visible_record_instances(self) -> Dict[str, Any]:
        record_instances, _ = get_all_records_from_json(self._state)
        return record_instances
