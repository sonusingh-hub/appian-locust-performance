import logging
import re

from utils.waits import small_wait
from utils.adaptive_wait import AdaptiveWait
from datetime import date as dt_date


log = logging.getLogger(__name__)


def _iter_component_tree(component):
    if isinstance(component, dict):
        yield component
        for value in component.values():
            yield from _iter_component_tree(value)
    elif isinstance(component, list):
        for item in component:
            yield from _iter_component_tree(item)


def _iter_component_tree_with_ancestors(component, ancestors=None):
    if ancestors is None:
        ancestors = []

    if isinstance(component, dict):
        yield component, ancestors
        next_ancestors = ancestors + [component]
        for value in component.values():
            yield from _iter_component_tree_with_ancestors(value, next_ancestors)
    elif isinstance(component, list):
        for item in component:
            yield from _iter_component_tree_with_ancestors(item, ancestors)


def _extract_component_text(component):
    parts = []
    common_text_keys = [
        "label",
        "tooltip",
        "aria-label",
        "ariaLabel",
        "accessibilityText",
        "placeholder",
        "altText",
        "testLabel",
    ]

    for node in _iter_component_tree(component):
        if not isinstance(node, dict):
            continue

        for key in common_text_keys:
            value = node.get(key)
            if isinstance(value, str) and value:
                parts.append(value)

        if "caption" in node and isinstance(node["caption"], str) and node["caption"]:
            parts.append(node["caption"])

        if "text" in node and isinstance(node["text"], str) and node["text"]:
            parts.append(node["text"])

        if "#v" in node and isinstance(node["#v"], str) and node["#v"].strip():
            parts.append(node["#v"])

    return " ".join(part.strip() for part in parts if part and part.strip())


def _extract_node_text(node):
    if not isinstance(node, dict):
        return ""

    parts = []
    text_keys = [
        "label",
        "tooltip",
        "aria-label",
        "ariaLabel",
        "accessibilityText",
        "placeholder",
        "altText",
        "testLabel",
        "caption",
        "text",
    ]

    for key in text_keys:
        value = node.get(key)
        if isinstance(value, str) and value:
            parts.append(value)

    direct_value = node.get("#v")
    if isinstance(direct_value, str) and direct_value.strip():
        parts.append(direct_value)

    return " ".join(part.strip() for part in parts if part and part.strip())


def _normalize_text(value):
    if not isinstance(value, str):
        return ""

    return " ".join(value.split()).casefold()


def has_component_label(uiform, label, is_test_label=False):
    if not uiform or not isinstance(label, str) or not label:
        return False

    key = "testLabel" if is_test_label else "label"

    for component in _iter_component_tree(uiform._state):
        if not isinstance(component, dict):
            continue

        if component.get(key) == label:
            return True

    return False


def has_component_text(uiform, text):
    if not uiform or not isinstance(text, str) or not text:
        return False

    target = _normalize_text(text)
    if not target:
        return False

    for component in _iter_component_tree(uiform._state):
        if not isinstance(component, dict):
            continue

        component_text = _normalize_text(_extract_node_text(component))
        if component_text and target in component_text:
            return True

        aggregate_text = _normalize_text(_extract_component_text(component))
        if aggregate_text and target in aggregate_text:
            return True

    return False


def has_component_icon(uiform, icon_name):
    if not uiform or not isinstance(icon_name, str) or not icon_name:
        return False

    target = _normalize_text(icon_name)
    if not target:
        return False

    for component in _iter_component_tree(uiform._state):
        if not isinstance(component, dict):
            continue

        component_icon = _normalize_text(component.get("icon", ""))
        if component_icon and component_icon == target:
            return True

    return False


def _linked_item_matches_caption(component, caption):
    target = _normalize_text(caption)
    if not target:
        return False

    searchable_texts = []
    searchable_texts.append(_normalize_text(_extract_component_text(component)))
    searchable_texts.append(_normalize_text(component.get("accessibilityText", "")))

    values = component.get("values")
    if isinstance(values, dict):
        searchable_texts.append(_normalize_text(values.get("caption", "")))

    for text in searchable_texts:
        if not text:
            continue

        if text == target:
            return True

        if re.search(rf"\b{re.escape(target)}\b", text):
            return True

    return False


def _run_uiform_action(action_name, action_function, timeout=10, poll_interval=0.5):
    log.info("UI action start: %s", action_name)

    updated_uiform = None

    def _action():
        nonlocal updated_uiform
        updated_uiform = action_function()
        return updated_uiform

    completed = AdaptiveWait.wait_for_dropdown_action(
        _action,
        timeout=timeout,
        poll_interval=poll_interval
    )
    small_wait()

    if completed and updated_uiform is not None:
        log.info("UI action success: %s", action_name)
        return updated_uiform

    log.warning("UI action failed: %s", action_name)
    return None


def click_linked_item_by_caption(uiform, caption, timeout=10):
    if not uiform:
        return None

    def _action():
        for component in _iter_component_tree(uiform._state):
            if component.get("#t") != "LinkedItem":
                continue

            if not _linked_item_matches_caption(component, caption):
                continue

            link_component = component.get("link")
            if not link_component:
                return None

            new_state = uiform._dispatch_click(
                component=link_component,
                locust_label=f"{uiform.breadcrumb}.ClickLinkedItem.{caption}"
            )
            return uiform._reconcile_state(new_state, skipValidations=True)

        raise ValueError(f"LinkedItem with caption '{caption}' not found")

    return _run_uiform_action(
        f"click_linked_item_by_caption caption={caption}",
        _action,
        timeout=timeout
    )


def click_card_by_text(uiform, text, timeout=10):
    if not uiform:
        return None

    normalized_target = " ".join(text.split()).casefold()

    def _action():
        for component in _iter_component_tree(uiform._state):
            if component.get("#t") != "CardLayout":
                continue

            link_component = component.get("link")
            if not link_component:
                continue

            component_text = " ".join(_extract_component_text(component).split()).casefold()
            if normalized_target not in component_text:
                continue

            new_state = uiform._dispatch_click(
                component=link_component,
                locust_label=f"{uiform.breadcrumb}.ClickCardByText.{text}"
            )
            return uiform._reconcile_state(new_state, skipValidations=True)

        raise ValueError(f"CardLayout with text '{text}' not found")

    return _run_uiform_action(
        f"click_card_by_text text={text}",
        _action,
        timeout=timeout
    )


def click_clickable_by_text(uiform, text, timeout=10):
    if not uiform:
        return None

    normalized_target = _normalize_text(text)

    def _resolve_clickable_component(node, ancestors):
        link_component = node.get("link")
        if link_component:
            return link_component

        if isinstance(node.get("saveInto"), list) and node.get("saveInto"):
            return node

        for ancestor in reversed(ancestors):
            if not isinstance(ancestor, dict):
                continue

            link_component = ancestor.get("link")
            if link_component:
                return link_component

            if isinstance(ancestor.get("saveInto"), list) and ancestor.get("saveInto"):
                return ancestor

        return None

    def _action():
        for component, ancestors in _iter_component_tree_with_ancestors(uiform._state):
            if not isinstance(component, dict):
                continue

            component_text = _normalize_text(_extract_node_text(component))
            aggregate_text = _normalize_text(_extract_component_text(component))
            accessibility_text = _normalize_text(component.get("accessibilityText", ""))
            aria_label_text = _normalize_text(component.get("aria-label", ""))
            camel_aria_label_text = _normalize_text(component.get("ariaLabel", ""))

            matches_text = (
                (component_text and normalized_target in component_text)
                or (aggregate_text and normalized_target in aggregate_text)
                or (accessibility_text and normalized_target in accessibility_text)
                or (aria_label_text and normalized_target in aria_label_text)
                or (camel_aria_label_text and normalized_target in camel_aria_label_text)
            )
            if not matches_text:
                continue

            clickable_component = _resolve_clickable_component(component, ancestors)

            if not clickable_component:
                continue

            new_state = uiform._dispatch_click(
                component=clickable_component,
                locust_label=f"{uiform.breadcrumb}.ClickClickableByText.{text}"
            )
            return uiform._reconcile_state(new_state, skipValidations=True)

        raise ValueError(f"Clickable component with text '{text}' not found")

    return _run_uiform_action(
        f"click_clickable_by_text text={text}",
        _action,
        timeout=timeout
    )


def click_clickable_by_icon(uiform, icon_name, timeout=10):
    if not uiform:
        return None

    normalized_icon = _normalize_text(icon_name)

    def _action():
        for component in _iter_component_tree(uiform._state):
            if not isinstance(component, dict):
                continue

            icon_value = _normalize_text(component.get("icon", ""))
            if icon_value != normalized_icon:
                continue

            if not (isinstance(component.get("saveInto"), list) and component.get("saveInto")):
                continue

            new_state = uiform._dispatch_click(
                component=component,
                locust_label=f"{uiform.breadcrumb}.ClickClickableByIcon.{icon_name}"
            )
            return uiform._reconcile_state(new_state, skipValidations=True)

        raise ValueError(f"Clickable component with icon '{icon_name}' not found")

    return _run_uiform_action(
        f"click_clickable_by_icon icon={icon_name}",
        _action,
        timeout=timeout
    )


def select_dropdown(uiform, label, value, timeout=10):
    if not uiform:
        return None

    return _run_uiform_action(
        f"select_dropdown label={label} value={value}",
        lambda: uiform.select_dropdown_item(
            label=label,
            choice_label=value
        ),
        timeout=timeout
    )


def select_dropdown_test_label(uiform, test_label, value, timeout=10):
    if not uiform:
        return None

    return _run_uiform_action(
        f"select_dropdown_test_label test_label={test_label} value={value}",
        lambda: uiform.select_dropdown_item(
            label=test_label,
            choice_label=value,
            is_test_label=True,
        ),
        timeout=timeout,
    )


def select_dropdown_by_index(uiform, index, value, timeout=10):
    if not uiform:
        return None

    return _run_uiform_action(
        f"select_dropdown_by_index index={index} value={value}",
        lambda: uiform.select_dropdown_item_by_index(
            index=index,
            choice_label=value,
        ),
        timeout=timeout,
    )


def select_multi_dropdown(uiform, label, values, timeout=10):
    if not uiform:
        return None

    if isinstance(values, str):
        values = [values]

    return _run_uiform_action(
        f"select_multi_dropdown label={label} values={values}",
        lambda: uiform.select_multi_dropdown_item(
            label=label,
            choice_label=values
        ),
        timeout=timeout
    )


def get_multi_dropdown_choices(uiform, label, is_test_label=False):
    if not uiform:
        return []

    attribute_to_find = "testLabel" if is_test_label else "label"

    for component in _iter_component_tree(uiform._state):
        if not isinstance(component, dict):
            continue

        if component.get("#t") not in ("MultipleDropdownField", "MultipleDropdownWidget"):
            continue

        if component.get(attribute_to_find) != label:
            continue

        choices = component.get("choices")
        if not isinstance(choices, list):
            return []

        return [choice for choice in choices if isinstance(choice, str) and choice.strip()]

    return []


def click_button(uiform, label, is_test_label=False, timeout=10):
    if not uiform:
        return None

    return _run_uiform_action(
        f"click_button label={label} is_test_label={is_test_label}",
        lambda: uiform.click(
            label=label,
            is_test_label=is_test_label
        ),
        timeout=timeout
    )


def fill_text_field(uiform, label, value, is_test_label=False, timeout=10):
    if not uiform:
        return None

    return _run_uiform_action(
        f"fill_text_field label={label} value={value} is_test_label={is_test_label}",
        lambda: uiform.fill_text_field(
            label=label,
            value=value,
            is_test_label=is_test_label
        ),
        timeout=timeout
    )


def click_field(uiform, label, is_test_label=False, timeout=10):
    if not uiform:
        return None

    return _run_uiform_action(
        f"click_field label={label} is_test_label={is_test_label}",
        lambda: uiform.click(
            label=label,
            is_test_label=is_test_label
        ),
        timeout=timeout
    )


def click_record_list_action(uiform, label, timeout=10):
    if not uiform:
        return None

    if not hasattr(uiform, "click_record_list_action"):
        log.warning(
            "UI form type %s does not support click_record_list_action for label '%s'.",
            type(uiform).__name__,
            label,
        )
        return None

    return _run_uiform_action(
        f"click_record_list_action label={label}",
        lambda: uiform.click_record_list_action(
            label=label,
        ),
        timeout=timeout
    )


def click_start_process_link(uiform, label, is_test_label=False, timeout=10):
    if not uiform:
        return None

    if not hasattr(uiform, "click_start_process_link"):
        log.warning(
            "UI form type %s does not support click_start_process_link for label '%s'.",
            type(uiform).__name__,
            label,
        )
        return None

    return _run_uiform_action(
        f"click_start_process_link label={label} is_test_label={is_test_label}",
        lambda: uiform.click_start_process_link(
            label=label,
            is_test_label=is_test_label,
        ),
        timeout=timeout,
    )


def fill_picker_field(
    uiform,
    label,
    value,
    identifier="#v",
    format_test_label=False,
    timeout=10,
):
    if not uiform:
        return None

    return _run_uiform_action(
        (
            f"fill_picker_field label={label} value={value} "
            f"identifier={identifier} format_test_label={format_test_label}"
        ),
        lambda: uiform.fill_picker_field(
            label=label,
            value=value,
            identifier=identifier,
            format_test_label=format_test_label,
        ),
        timeout=timeout
    )

def fill_date_field(uiform, label, year, month, day, timeout=10):
    if not uiform:
        return None

    return _run_uiform_action(
        f"fill_date_field label={label} value={year:04d}-{month:02d}-{day:02d}",
        lambda: uiform.fill_date_field(
            label=label,
            date_input=dt_date(year=year, month=month, day=day)
        ),
        timeout=timeout
    )
