import os
import sys
from pathlib import Path
from uuid import uuid4

if __package__ in (None, ""):
    # Launched as `python ui/tui.py` or `textual run ui/tui.py`, which puts
    # `ui/` on sys.path. The project root is the import root, so add it.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from textual.app import App
from textual.widgets import Input, Footer, Static
from textual.containers import VerticalScroll
from pydantic import SecretStr

from ui.widgets.tool_call_bar import ToolCallBar
from ui.widgets.user_query_widget import UserQueryWidget
from agents.herr import MainAgent
from prompts.main import GeneralPrompts
from handlers.handle_prompt_input import handlePrompt


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

    CSS_PATH = ["../style/tool_call_style.tcss", "../style/main.tcss", "../style/user_query_style.tcss"]

    

    def on_mount(self):

        feed = self.query_exactly_one('#content_sheet', VerticalScroll)
        feed.mount(ToolCallBar(title="something something"))




    def compose(self):

        yield VerticalScroll(id = "content_sheet")
        yield Input(placeholder = "", id = "user_input")
        yield Footer()


    async def on_input_submitted(self, event: Input.Submitted):

        if event.value:

            user_prompt = event.value
            feed = self.query_exactly_one('#content_sheet', VerticalScroll)
            feed.mount(UserQueryWidget(user_query= user_prompt))
            event.input.value = ""


            

            handlePrompt(self.agent, user_prompt= user_prompt)



if __name__ == "__main__":

    app = SiftApp()
    app.run()