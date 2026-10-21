from textual.app import App
from textual.widgets import Input, Footer, Static
from textual.containers import VerticalScroll
from widgets.tool_call_bar import ToolCallBar
from widgets.user_query_widget import UserQueryWidget


class SiftApp(App):

    CSS_PATH = ["../style/tool_call_style.tcss", "../style/main.tcss", "../style/user_query_style.tcss"]

    def on_mount(self):

        feed = self.query_exactly_one('#content_sheet', VerticalScroll)
        feed.mount(ToolCallBar(title="something something"))




    def compose(self):

        yield VerticalScroll(id = "content_sheet")
        yield Input(placeholder = "", id = "user_input")
        yield Footer()


    async def on_input_submitted(self, event: Input.Submitted):

        user_prompt = event.value
        feed = self.query_exactly_one('#content_sheet', VerticalScroll)
        feed.mount(UserQueryWidget(user_query= user_prompt))
        event.input.value = ""




if __name__ == "__main__":

    app = SiftApp()
    app.run()