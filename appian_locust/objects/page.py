from enum import Enum


class PageType(Enum):
    ACTION: str = "action"
    REPORT: str = "report"
    RECORD: str = "recordType"
    INTERFACE: str = "interface"


class Page:
    """
    Class representing a single Page within a site
    """

    def __init__(self, page_name: str, page_type: PageType) -> None:
        self.page_name = page_name
        self.page_type = page_type

    def __str__(self) -> str:
        return f"Page(name={self.page_name},type={self.page_type})"

    def __repr__(self) -> str:
        return self.__str__()
