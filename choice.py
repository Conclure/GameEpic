import typing

class Choice():
    def __init__(self):
        pass
        self.choices = []
        self.title = "N/A"
        self.preprocessors = []

    def add_preprocessor(self,callback: typing.Callable[[],None]):
        self.preprocessors.append(callback)

    def set_title(self,title: str):
        self.title = title

    def add_option(self,name: str):
        self.choices.append(name)

    def on_invalid_option(self,callback: typing.Callback[[],bool]):
        self.fail_callback = callback

    def invoke(self):
        pass
