from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown, Static, Header, Footer

class ToolCallBlock(Static):
    """Widget representing a tool execution block."""
    def __init__(self, tool_name: str, **kwargs):
        super().__init__(f"🛠️ [bold yellow]Executing {tool_name}...[/bold yellow]", **kwargs)

    def mark_complete(self, result_summary: str):
        self.update(f"✅ [bold green]Tool Complete:[/bold green] {result_summary}")

class CodingTUI(App):
    CSS = """
    VerticalScroll {
        height: 1fr;
        border: solid green;
    }
    .user-msg {
        background: $accent-muted;
        margin: 1;
        padding: 1;
    }
    .assistant-msg {
        background: $panel;
        margin: 1;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="chat_feed")
        yield Input(placeholder="Ask your assistant...", id="user_input")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_text = event.value
        feed = self.query_one("#chat_feed", VerticalScroll)

        # 1. Mount user query
        feed.mount(Static(f"👤 {user_text}", classes="user-msg"))
        event.input.value = ""

        # 2. Trigger worker stream
        self.process_llm_stream(user_text)

    @work(exclusive=True)
    async def process_llm_stream(self, user_text: str) -> None:
        feed = self.query_one("#chat_feed", VerticalScroll)

        # Mount assistant text container
        response_widget = Markdown("", classes="assistant-msg")
        await feed.mount(response_widget)

        # Example: Simulating tool execution
        tool_widget = ToolCallBlock("bash_executor")
        await feed.mount(tool_widget)
        feed.scroll_end()

        # Simulate tool completion
        tool_widget.mark_complete("Executed 1 command successfully")

        # Simulate streaming text
        full_text = ""
        chunks = ["Here is ", "the response ", "to your ", "coding request."]
        for chunk in chunks:
            full_text += chunk
            response_widget.update(full_text)
            feed.scroll_end()

if __name__ == "__main__":
    app = CodingTUI()
    app.run()