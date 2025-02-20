from enum import Enum
from typing import Any, Dict, Optional

from .._interactor import _Interactor
from ..client_mode import ClientMode
from ..uiform import DesignObjectUiForm

from ..utilities.helper import (find_component_by_attribute_in_dict, find_component_by_type_and_attribute_and_index_in_dict)

class SourceType(Enum):
    LIVE_VIEW = "LIVE_VIEW"
    PALETTE = "PALETTE"
    ADD_COMPONENT_HELPER = "ADD_COMPONENT_HELPER"

class DropType(Enum):
    EMPTY_LIVE_VIEW = "EMPTY_LIVE_VIEW"
    PLACEHOLDER = "PLACEHOLDER"
    COMPONENT = "COMPONENT"

class InterfaceDesignerUiForm(DesignObjectUiForm):

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "InterfaceDesignerUi"):
        super().__init__(interactor, state, breadcrumb)
        interactor.set_client_mode(client_mode=ClientMode.INTERFACE_DESIGN)

    def select_component(self, component_label: str) -> None:
        component_id, _ = self.__get_live_view_component_info(component_label)
        new_value = {
            "action": "HIGHLIGHT_COMPONENT",
            "id": component_id
        }
        self.__send_interface_designer_manager_request(new_value, f"Select {component_label}")

    def drag_and_drop_from_palette_to_empty_live_view(self, source_palette_label: str) -> None:
        new_value = self.__get_palette_to_empty_live_view_save_value(source_palette_label)
        self.__send_interface_designer_manager_request(new_value,f"Drag '{source_palette_label}' from the Palette and drop in Empty Live View")

    def drag_and_drop_from_palette_to_component(self, source_palette_label: str, target_component: str, add_above: bool) -> None:
        new_value = self.__get_palette_to_component_save_value(source_palette_label, target_component, add_above)
        direction = "above" if add_above else "below"
        self.__send_interface_designer_manager_request(new_value,f"Drag '{source_palette_label}' from the Palette and drop {direction} {target_component}")

    def drag_and_drop_from_palette_to_placeholder(self, source_palette_label: str, parent_target_component: str) -> None:
        new_value = self.__get_palette_to_placeholder_save_value(source_palette_label, parent_target_component)
        self.__send_interface_designer_manager_request(new_value,f"Drag '{source_palette_label}' from the Palette and drop in the placeholder of {parent_target_component}")

    def drag_and_drop_from_live_view_to_component(self, source_component: str, target_component: str, add_above: bool) -> None:
        new_value = self.__get_live_view_to_component_save_value(source_component, target_component, add_above)
        direction = "above" if add_above else "below"
        self.__send_interface_designer_manager_request(new_value,f"Drag {source_component} from the Live View and drop {direction} {target_component}")

    def drag_and_drop_from_live_view_to_placeholder(self, source_component: str, parent_target_component: str) -> None:
        new_value = self.__get_live_view_to_placeholder_save_value(source_component, parent_target_component)
        self.__send_interface_designer_manager_request(new_value,f"Drag {source_component} from the Live View and drop in the placeholder of {parent_target_component}")

    def __get_palette_component_info(self, source_palette_label: str) -> tuple[str, str]:
        component_palette_button = find_component_by_type_and_attribute_and_index_in_dict(self._state,
                                                                                          type="ComponentPaletteButton",
                                                                                          attribute="label",
                                                                                          value=source_palette_label)
        if component_palette_button is None:
            raise Exception(f"Could not find {source_palette_label} in the Component Palette")
        template_id = component_palette_button["templateId"]
        template_component_type = component_palette_button["templateComponentType"]
        return template_id, template_component_type

    def __get_live_view_component_info(self, component_label: str) -> tuple[str, str]:
        component_selector = find_component_by_attribute_in_dict("_iddesign_label", component_label, self._state)
        if component_selector is None:
            raise Exception(f"Could not find {component_label} in the Live View")
        component_id = component_selector["_iddesign_id"]
        component_type = component_selector["#t"]
        return component_id, component_type

    def __get_child_placeholder_info(self, parent_component_label: str) -> str:
        component_selector = find_component_by_attribute_in_dict("_iddesign_label", parent_component_label, self._state)
        if component_selector is None:
            raise Exception(f"Could not find {parent_component_label} in the Live View")
        child_list_id = component_selector["_iddesign_childComponentListIds"].split(" ")[0] # For now, assume always the first id
        return child_list_id

    @staticmethod
    def __get_base_drag_and_drop_save_value(source_id: str, source_component_type: str, action: str, source_type: SourceType, drop_type: DropType) -> Dict[str, Any]:
        return {
            "shouldClearTempIds": True,
            "action": action,
            "sourceType": source_type.value,
            "targetType": drop_type.value,
            "newHighlightId": source_id,
            "sourceComponentTypes": [source_component_type]
        }

    def __get_palette_to_empty_live_view_save_value(self, source_palette_label: str) -> Dict[str, Any]:
        template_id, template_component_type = self.__get_palette_component_info(source_palette_label)
        temp_id = "1-2"
        base_value = self.__get_base_drag_and_drop_save_value(temp_id, template_component_type, "UPDATE", SourceType.PALETTE, DropType.EMPTY_LIVE_VIEW)
        new_value = base_value | {
            "paletteSearchTerm": "",
            "isUserInterface": False,
            "tempNodeMap": {
                temp_id: []
            },
            "templateId": template_id
        }
        return new_value

    def __get_palette_to_component_save_value(self, source_palette_label: str, target_component: str, add_above: bool) -> Dict[str, Any]:
        template_id, template_component_type = self.__get_palette_component_info(source_palette_label)
        target_component_id, target_component_type = self.__get_live_view_component_info(target_component)
        temp_id = "1-2"
        action = "ADD_ABOVE" if add_above else "ADD_BELOW"
        base_value = self.__get_base_drag_and_drop_save_value(temp_id, template_component_type, action, SourceType.PALETTE,
                                                              DropType.COMPONENT)
        new_value = base_value | {
            "paletteSearchTerm": "",
            "isUserInterface": False,
            "tempNodeMap": {
                temp_id: []
            },
            "templateId": template_id,
            "targetComponentTypes": [target_component_type],
            "targetNodeId": target_component_id
        }
        return new_value

    def __get_palette_to_placeholder_save_value(self, source_palette_label: str, parent_target_component: str) -> Dict[str, Any]:
        template_id, template_component_type = self.__get_palette_component_info(source_palette_label)
        placeholder_id = self.__get_child_placeholder_info(parent_target_component)
        temp_id = "1-2"
        base_value = self.__get_base_drag_and_drop_save_value(temp_id, template_component_type, "CUT_PASTE_ABOVE", SourceType.PALETTE,
                                                              DropType.COMPONENT)
        new_value = base_value | {
            "paletteSearchTerm": "",
            "isUserInterface": False,
            "tempNodeMap": {
                temp_id: []
            },
            "templateId": template_id,
            "targetComponentTypes": [],
            "targetNodeId": placeholder_id
        }
        return new_value

    def __get_live_view_to_component_save_value(self, source_component: str, target_component: str, add_above: bool) -> Dict[str, Any]:
        source_component_id, source_component_type = self.__get_live_view_component_info(source_component)
        target_component_id, target_component_type = self.__get_live_view_component_info(target_component)
        action = "CUT_PASTE_ABOVE" if add_above else "CUT_PASTE_BELOW"
        base_value = self.__get_base_drag_and_drop_save_value(source_component_id, source_component_type, action, SourceType.LIVE_VIEW, DropType.COMPONENT)
        new_value = base_value | {
            "targetComponentTypes": [target_component_type],
            "targetNodeId": target_component_id,
            "cutNodeId": source_component_id
        }
        return new_value

    def __get_live_view_to_placeholder_save_value(self, source_component: str, parent_target_component: str) -> Dict[str, Any]:
        source_component_id, source_component_type = self.__get_live_view_component_info(source_component)
        placeholder_id = self.__get_child_placeholder_info(parent_target_component)
        base_value = self.__get_base_drag_and_drop_save_value(source_component_id, source_component_type, "CUT_PASTE_ABOVE", SourceType.LIVE_VIEW, DropType.PLACEHOLDER)
        new_value = base_value | {
            "targetComponentTypes": [],
            "targetNodeId": placeholder_id,
            "cutNodeId": source_component_id
        }
        return new_value

    def __send_interface_designer_manager_request(self, new_value: Dict[str, Any], locust_label: str) -> None:
        interface_designer_manager_component = \
            find_component_by_type_and_attribute_and_index_in_dict(self._state, type="InterfaceDesignerManager")
        new_value_dictionary = {
            "#t": "Dictionary",
            "#v": new_value
        }
        new_state = self._interactor.click_generic_element(post_url=self.form_url,
                                                           component=interface_designer_manager_component,
                                                           context=self.context,
                                                           uuid=self.uuid,
                                                           new_value=new_value_dictionary,
                                                           label=locust_label)
        self._reconcile_state(new_state, skipValidations=True)
