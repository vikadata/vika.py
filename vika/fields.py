"""
暂时没用
"""


class BaseField:
    def set_value(self, value):
        """
        """
        pass


class TextField(BaseField):
    _type = "SingleText"


class AttachmentField(BaseField):
    _type = "Attachment"

    def set_value(self, value):
        pass


class LinkField(BaseField):
    _type = "Link"
