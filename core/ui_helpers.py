from utils.waits import small_wait
from utils.adaptive_wait import AdaptiveWait


def select_dropdown(uiform, label, value):
    if not uiform:
        return None

    updated_uiform = None

    def _action():
        nonlocal updated_uiform
        updated_uiform = uiform.select_dropdown_item(
            label=label,
            choice_label=value
        )
        return updated_uiform

    AdaptiveWait.wait_for_dropdown_action(_action, timeout=10, poll_interval=0.5)
    small_wait()
    return updated_uiform


def select_multi_dropdown(uiform, label, values):
    if not uiform:
        return None

    if isinstance(values, str):
        values = [values]

    updated_uiform = None

    def _action():
        nonlocal updated_uiform
        updated_uiform = uiform.select_multi_dropdown_item(
            label=label,
            choice_label=values
        )
        return updated_uiform

    AdaptiveWait.wait_for_dropdown_action(_action, timeout=10, poll_interval=0.5)
    small_wait()
    return updated_uiform


def click_button(uiform, label, is_test_label=False):
    if not uiform:
        return None

    updated_uiform = None

    def _action():
        nonlocal updated_uiform
        updated_uiform = uiform.click(
            label=label,
            is_test_label=is_test_label
        )
        return updated_uiform

    AdaptiveWait.wait_for_dropdown_action(_action, timeout=10, poll_interval=0.5)
    small_wait()
    return updated_uiform