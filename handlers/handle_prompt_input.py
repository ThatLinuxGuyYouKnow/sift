from uuid import uuid4
from agents.herr import MainAgent
import os
from dotenv import load_dotenv
from ui.widgets.tool_call_bar import ToolCallBar
from ui.widgets.agent_response import AgentResponseWidget


def handlePrompt(agent: MainAgent, user_prompt : str):

    for chunk in agent(prompt = user_prompt):

        if chunk['type'] == 'token':

            yield AgentResponseWidget(chunk['content'])




