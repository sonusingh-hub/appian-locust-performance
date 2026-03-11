import time


class AdaptiveWait:

    @staticmethod
    def wait_for(condition_function, timeout=10, poll_interval=0.5):
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                if condition_function():
                    return True
            except Exception:
                pass

            time.sleep(poll_interval)

        return False

    @staticmethod
    def wait_for_dropdown_action(action_function, timeout=10, poll_interval=0.5):
        return AdaptiveWait.wait_for(
            lambda: action_function() is not None,
            timeout=timeout,
            poll_interval=poll_interval
        )