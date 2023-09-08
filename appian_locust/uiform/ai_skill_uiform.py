from typing import Any, Dict
from .._rdo_interactor import _RDOInteractor
from .._locust_error_handler import raises_locust_error
from ..uiform import SailUiForm


class AISkillUiForm(SailUiForm):

    def __init__(self, interactor: _RDOInteractor, state: Dict[str, Any], breadcrumb: str = "AISkillUi"):
        rdo_interactor = interactor
        super().__init__(rdo_interactor, state, breadcrumb)

