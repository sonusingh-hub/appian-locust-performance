import time
import logging


log = logging.getLogger(__name__)


class AdaptiveWait:

    @staticmethod
    def wait_for(condition_function, timeout=10, poll_interval=0.5):
        start_time = time.time()
        last_exception = None

        while time.time() - start_time < timeout:
            try:
                if condition_function():
                    return True
            except Exception as exc:
                last_exception = exc

            time.sleep(poll_interval)

        if last_exception is not None:
            log.warning(
                "Adaptive wait timed out after %.1fs; last exception: %s",
                timeout,
                repr(last_exception)
            )

        return False

    @staticmethod
    def wait_for_dropdown_action(action_function, timeout=10, poll_interval=0.5):
        return AdaptiveWait.wait_for(
            lambda: action_function() is not None,
            timeout=timeout,
            poll_interval=poll_interval
        )
