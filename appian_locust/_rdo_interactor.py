from typing import Any, Dict, Optional, Tuple
from requests import Response
from ._interactor import _Interactor
from ._locust_error_handler import raises_locust_error
from ._save_request_builder import save_builder
from .utilities.helper import find_component_by_attribute_in_dict, extract_all_by_label
from locust.clients import HttpSession, ResponseContextManager
import time
import base64
import json


class _RDOInteractor(_Interactor):
    def __init__(self, interactor: _Interactor, rdo_host: str):
        super().__init__(interactor.client, interactor.host, interactor.portals_mode, interactor._request_timeout)
        self.rdo_host = rdo_host
        self.last_auth_time = float(0)
        self.auth = interactor.auth
        self.jwt_token, self.rdo_csrf_token = self.fetch_jwt_token()
        self.v1_post_request(jwt_token=self.jwt_token, rdo_csrf_token=self.rdo_csrf_token)

    def get_interaction_host(self) -> str:
        return self.rdo_host

    def fetch_jwt_token(self) -> Tuple:
        uri_full = f"{self.host}/suite/rfx/bff-token"
        payload = {
            "resource": "aiSkill"
        }
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en_US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "origin": self.host,
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-APPIAN-CSRF-TOKEN": self.client.cookies.get("__appianCsrfToken", "")
        }
        resp = super().post_page(uri=uri_full, headers=headers, payload=payload)
        self.last_auth_time = time.time()
        jwt_token = resp.json()["token"]
        jwt_token_split = jwt_token.split('.')[1] + '=='
        string_decoded_jwt = base64.b64decode(s=jwt_token_split).decode('utf-8')
        rdo_csrf_token = json.loads(string_decoded_jwt)['csrf']
        return jwt_token, rdo_csrf_token

    def v1_post_request(self, jwt_token: str, rdo_csrf_token: str) -> Any:
        v1_uri = f"{self.rdo_host}/rdo-server/DesignObjects/InterfaceAuthentication/v1"
        v1_payload = f"access_token={jwt_token}"
        v1_headers = {
            "authority": f"{self.rdo_host}",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en_US,en;q=0.9",
            "origin": self.host,
            "referer": f"{self.host}/",
            "cookie": f"XSRF-TOKEN={rdo_csrf_token}; JWT_TOKEN={jwt_token}",
            "content-type": "application/x-www-form-urlencoded"
        }
        v1_response = super().post_page(uri=v1_uri, payload=v1_payload, headers=v1_headers)
        v1_response.raise_for_status()
        return None

    def setup_rdo_ui_request_headers(self, jwt_token: str, rdo_csrf_token: str) -> dict:
        ui_headers = {
            "authority": f"{self.rdo_host}",
            "accept": "application/vnd.appian.tv.ui+json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/vnd.appian.tv+json",
            "origin": f"{self.rdo_host}",
            "referer": f"{self.rdo_host}/rdo-server/DesignObjects/LoadCreateDialogInterface/v1?applicationPrefix=",
            "cookie": f"XSRF-TOKEN={rdo_csrf_token}; JWT_TOKEN={jwt_token}",
            "x-appian-csrf-token": f"{rdo_csrf_token}",
            "x-appian-ui-state": "stateful",
            "x-appian-features": f"{self.client.feature_flag}",
            "x-appian-features-extended": f"{self.client.feature_flag_extended}",
            "x-appian-suppress-www-authenticate": "true",
            "x-client-mode": "SAIL_LIBRARY",
            "x-appian-user-locale": "en_US",
            "x-appian-user-timezone": "",
            "x-appian-user-calendar": "",
            "x-appian-initial-form-factor": "PHONE"
        }
        return ui_headers

    # move to fetch method if not used anywhere else by the end of RDO Epic
    def ai_skill_creation_payload(self, jwt_token: str, app_prefix: str) -> dict:
        payload = {
            "initialBindings": {"flow!jwt": f"{jwt_token}", "flow!applicationPrefix": f"{app_prefix}"},
            "#t": "Map"
             }
        return payload

    def ai_skill_creation_save_payload(self, state: Dict[str, Any], object_uuid: str) -> dict:
        component = find_component_by_attribute_in_dict(attribute="testLabel", value="customCreateDialog", component_tree=state)
        value = {
            "#t": "Text",
            "#v": "{\"action\":\"COMPLETE_SAVE\",\"objectUuid\":\"" + object_uuid + "\"}"
        }
        context = state["context"]
        uuid = state["uuid"]
        payload = save_builder() \
            .component(component) \
            .value(value) \
            .context(context) \
            .uuid(uuid) \
            .build()
        return payload

    def post_page(self, uri: str,
                  payload: Any = {},
                  headers: Optional[Dict[str, Any]] = None,
                  label: Optional[str] = None,
                  files: Optional[dict] = None,
                  check_login: bool = True) -> Response:
        if time.time() - self.last_auth_time > 25:
            self.jwt_token, self.rdo_csrf_token = self.fetch_jwt_token()
            self.v1_post_request(self.jwt_token, self.rdo_csrf_token)
        if headers is None:
            headers = self.setup_rdo_ui_request_headers(self.jwt_token, rdo_csrf_token=self.rdo_csrf_token)
        return super().post_page(uri, payload, headers, label, files, check_login)

    @raises_locust_error
    def fetch_ai_skill_creation_dialog_json(self, app_prefix: str, locust_request_label: str = "AISkill.CreateDialog") -> Dict[str, Any]:
        headers = self.setup_rdo_ui_request_headers(jwt_token=self.jwt_token, rdo_csrf_token=self.rdo_csrf_token)
        headers["x-http-method-override"] = "PUT"
        payload = self.ai_skill_creation_payload(jwt_token=self.jwt_token, app_prefix=app_prefix)
        uri = f"{self.rdo_host}/sail-server/SYSTEM_SYSRULES_aiSkillCreateDialog/ui"
        return self.post_page(uri=uri, payload=payload, headers=headers, label=locust_request_label).json()

    @raises_locust_error
    def fetch_ai_skill_creation_save_dialog_json(self, state: Dict[str, Any], rdo_state: Dict[str, Any], locust_request_label: str = "AISkill.CreationSaveDialog") -> Dict[str, Any]:
        object_uuid = extract_all_by_label(obj=rdo_state, label="newObjectUuid")[0]
        payload = self.ai_skill_creation_save_payload(state=state, object_uuid=object_uuid)
        list_of_links = state["links"]
        for link_object in list_of_links:
            if link_object.get("rel") == "update":
                reeval_url = link_object.get("href", "")
                break
        headers = super().setup_sail_headers()
        headers["X-client-mode"] = "DESIGN"
        return super().post_page(uri=reeval_url, payload=payload, headers=headers).json()

    # @raises_locust_error
    # def fetch_ai_skill_designer_json():
