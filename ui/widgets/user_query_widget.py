from textual.widgets import Static, Label
from textual.containers import Horizontal


class UserQueryWidget(Horizontal):


    def __init__(self, user_query: str, **kwargs):

        kwargs.setdefault("classes", "user-query-bar")
        super().__init__(**kwargs)
        self._user_query = user_query

    def compose(self):

        yield Static(self._user_query, classes=  'user-query')
        yield Label('user', classes = 'user-query-tag')
