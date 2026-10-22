from textual.widgets import Static, Label
from textual.containers import Horizontal
from rich.text import Text
class AgentResponseWidget(Horizontal):

    def __init__(self, **kwargs):

        kwargs.setdefault('classes', 'agent-response')
        super().__init__(**kwargs)
        self._buffer = ""

    def compose(self):

        
        yield Label(classes= 'agent-response-tag',content= 'agent')
        yield Static(classes='agent-response-body', content= '')


    def update(self, text: str):

        self._buffer += text
        self.query_one('#agent-response-body', Static).update(Text(self._buffer))




