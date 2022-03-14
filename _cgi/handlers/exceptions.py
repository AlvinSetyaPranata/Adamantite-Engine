class Template_Not_Found(Exception):
    def __init__(self, *msg):
        return super().__init__(*msg)


class Invalid_Component(Exception):
    def __init__(self, *msg):
        return super().__init__(*msg)


class Invalid_View(Exception):
    def __init__(self, *msg):
        return super().__init__(*msg)
