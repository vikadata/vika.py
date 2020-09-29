# 暂时没用
class BaseField:
    pass


class TextField(BaseField):
    _type = "text"


class AttachmentField(BaseField):
    _type = "attachment"


class LinkField(BaseField):
    _type = "link"
