from typing import Dict
from .page import Page


class Site:
    """
    Class representing a single site, as well as its pages
    """

    def __init__(self, name: str, display_name: str, pages: Dict[str, Page]):
        self.name = name
        self.display_name = display_name
        self.pages = pages

    def __str__(self) -> str:
        return f"Site(name={self.name},pages=[{self.pages}])"

    def __repr__(self) -> str:
        return self.__str__()
