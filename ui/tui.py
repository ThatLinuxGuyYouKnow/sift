import os
import sys
from pathlib import Path
from uuid import uuid4



if __package__ in (None, ""):
    # Launched as `python ui/tui.py` or `textual run ui/tui.py`, which puts
    # `ui/` on sys.path. The project root is the import root, so add it.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ui.widgets.agent_response import AgentResponseWidget
from textual import work
from textual.app import App
from textual.widgets import Input, Footer, Static
from textual.containers import VerticalScroll
from pydantic import SecretStr

from ui.widgets.tool_call_bar import ToolCallBar
from ui.widgets.user_query_widget import UserQueryWidget
from agents.herr import MainAgent
from prompts.main import GeneralPrompts



class SiftApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #TODO : Read these from a config file
                   
        self.agent = MainAgent(
                        model = 'nvidia/nemotron-3.5-lightning-free',
                        api_key= SecretStr(os.environ['AI_GATEWAY_KEY']),
                        base_url= "https://ai-gateway.vercel.sh/v1",
                        thread_id= str(uuid4()),
                        system_prompt= GeneralPrompts.main_agent_prompt
                    )

    CSS_PATH = ["../style/tool_call_style.tcss", "../style/main.tcss", "../style/user_query_style.tcss", "../style/agent_response_style.tcss"]

    def on_mount(self):
        #immediately bring the input field into focus on entry

        inp = self.query_one('#user_input', Input)
        inp.focus()


    def compose(self):

        yield VerticalScroll(id = "content_sheet")
        yield Input(placeholder = "", id = "user_input")
        yield Footer()


    async def on_input_submitted(self, event: Input.Submitted):

        if event.value:

            user_prompt = event.value
            event.input.value = ""
            event.input.disabled = True
            feed = self.query_exactly_one('#content_sheet', VerticalScroll)
            await feed.mount(UserQueryWidget(user_query= user_prompt))
            # slide to the very end of the chat on a new prompt
            feed.scroll_end(animate = True)

            self.run_agent(user_prompt)



    @work(thread= True)
    def run_agent(self, prompt: str):

        response: AgentResponseWidget | None = None

        for event in self.agent(prompt):

            match event["type"]:

                case "token":

                    if response is None:
                        response = self.call_from_thread(self._new_response)

                    self.call_from_thread(response.update, event['content'])

                case "tool_call":

                    self.call_from_thread(self._add_tool_call, event['name'], event['args'])
        self.call_from_thread(self._finish)


    async def _new_response(self) -> AgentResponseWidget:

        feed = self.query_one("#content_sheet", VerticalScroll)
        widget = AgentResponseWidget()
        feed.mount(widget)
        feed.scroll_end(animate= True)

        return widget

    async def _add_tool_call(self, name: str, args: dict) -> None:

        feed = self.query_one('#content_sheet', VerticalScroll)
        widget = ToolCallBar(title = name, content = str(args))

        feed.mount(widget)

        feed.scroll_end()

    def _finish(self):
        "Agent turn has finished, so re-enable the input field"

        inp = self.query_one('#user_input', Input)

        inp.disabled = False
        #bring back into focus for users follow up
        inp.focus()










if __name__ == "__main__":

    app = SiftApp()
    app.run()