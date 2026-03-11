from utils.waits import small_wait


class BasePage:

    def __init__(self, taskset):
        self.taskset = taskset
        self.appian = taskset.appian
        self.client = taskset.client

    def visit(self, site_name, page_name):

        uiform = self.appian.visitor.visit_site(
            site_name=site_name,
            page_name=page_name
        )

        small_wait()

        return uiform