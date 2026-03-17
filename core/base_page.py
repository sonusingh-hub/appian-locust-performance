import logging
import time

from utils.waits import small_wait


log = logging.getLogger(__name__)


class BasePage:

    def __init__(self, taskset):
        self.taskset = taskset
        self.appian = taskset.appian
        self.client = taskset.client

    def visit(self, site_name, page_name):
        log.info("Visit page start: site=%s page=%s", site_name, page_name)
        start_time = time.perf_counter()

        try:
            uiform = self.appian.visitor.visit_site(
                site_name=site_name,
                page_name=page_name
            )
        except Exception:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            log.exception(
                "Visit page exception: site=%s page=%s elapsed_ms=%.1f",
                site_name,
                page_name,
                elapsed_ms
            )
            return None

        small_wait()
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        if uiform:
            log.info(
                "Visit page success: site=%s page=%s elapsed_ms=%.1f",
                site_name,
                page_name,
                elapsed_ms
            )
        else:
            log.warning(
                "Visit page failed: site=%s page=%s elapsed_ms=%.1f",
                site_name,
                page_name,
                elapsed_ms
            )

        return uiform
