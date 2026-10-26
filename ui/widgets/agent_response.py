from textual.widgets import Static, Label, Markdown
from textual.containers import Horizontal
from rich.text import Text
class AgentResponseWidget(Horizontal):

    def __init__(self, **kwargs):

        kwargs.setdefault('classes', 'agent-response')
        super().__init__(**kwargs)
        self._buffer = ""

    def compose(self):

        
        yield Label(classes= 'agent-response-tag',content= 'agent')
        yield Markdown(classes='agent-response-body', markdown= '')


    def update(self, text: str):

        self._buffer += text
        self.query_one('.agent-response-body', Markdown).update(self._buffer)




