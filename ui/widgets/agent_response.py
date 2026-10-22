from textual.widgets import Static, Label
from textual.containers import Horizontal

class AgentResponseWidget(Horizontal):

    def __init__(self, agent_response: str, **kwargs):

        kwargs.setdefault('classes', 'agent-response')
        super().__init__(**kwargs)
        self._agent_response = agent_response

    def compose(self):

        
        yield Label(classes= 'agent-response-tag',content= 'agent')
        yield Static(classes='user-query', content= self._agent_response)




