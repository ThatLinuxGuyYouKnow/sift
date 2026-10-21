from textual.containers import Vertical
from textual.widgets import Label, Static

class ToolCallBar(Vertical):

    def __init__(self, title: str = "Tool", content: str = "", **kwargs):
        kwargs.setdefault("id", "tool-bar")
        super().__init__(**kwargs)
        self._title = title
        self._body = content

    def compose(self):
        yield Label(self._title, id="tool-title")
        yield Static(self._body, id="tool-body")

    def set_title(self, title: str) -> None:
        self._title = title
        self.query_one("#tool-title", Label).update(title)

    def update_content(self, content: str) -> None:
        self._body = content
        self.query_one("#tool-body", Static).update(content)

    def append_content(self, chunk: str) -> None:
        self.update_content(self._body + chunk)
         




