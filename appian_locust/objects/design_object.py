from enum import Enum


class DesignObjectType(Enum):
    DATA_TYPE = 5
    DECISION = 6
    EXPRESSION_RULE = 8
    INTEGRATION = 12
    INTERFACE = 13
    RECORD_TYPE = 17
    SITE = 19
    WEB_API = 20


class DesignObject:
    """
    Class representing an Design Object
    """

    def __init__(self, name: str, opaque_id: str):
        self.name = name
        self.opaque_id = opaque_id

    def __str__(self) -> str:
        return f"DesignObject(name={self.name}, opaque_id={self.opaque_id})"

    def __repr__(self) -> str:
        return self.__str__()
