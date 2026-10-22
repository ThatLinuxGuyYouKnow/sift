from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage
from tools.search_tools import url_context, light_search, crawl_website
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from typing import Any
from pydantic import SecretStr
from dotenv import load_dotenv



load_dotenv()

TOOLS = [url_context, light_search, crawl_website]

class MainAgent():


    def __init__(self, model:str, api_key: SecretStr, base_url: str, thread_id : str, system_prompt: str, tools: list | None = None):

        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.tools = tools or TOOLS
        self.checkpointer = InMemorySaver()
        self.thread_id = thread_id
        self.system_prompt = system_prompt

        agent_model = ChatOpenAI(model=self.model, api_key= self.api_key, base_url= self.base_url )

        self.agent = create_agent(
                    checkpointer= self.checkpointer,
                    model=agent_model,
                    tools=self.tools,
                    system_prompt
                        =system_prompt,
                    middleware=[
                        HumanInTheLoopMiddleware(
                            description_prefix="Do you have permission to crawl this webpage? certain web-admins do not favour crawling",
                            interrupt_on={
                                'crawl_website': {'allowed_decisions': ["approve", "reject"]}
                            },
                        )
                    ],
        
        )

    @property

    def _config(self) -> Any:
        return {'configurable':{'thread_id':self.thread_id}}


    def _stream(self, agent_input:Any) :

        #largely based off https://docs.langchain.com/oss/python/langchain/streaming

        stream = self.agent.stream_events(agent_input, version = "v3", config = self._config)

        for kind, item in stream.interleave("messages", "tool_calls"):


            if kind == 'messages':

                for delta in item.text:

                    yield {'type':'token', 'content' : delta}


            elif kind == 'tool_calls':

                yield {'type' : 'tool_name' , 'content' : item.tool_name } 
                yield {'type' : 'tool_input', 'content' : item.input}


        # for mode, data in self.agent.stream(agent_input,config = self._config, stream_mode = ['messages', 'updates']):
        #     if mode == 'messages':
        #         chunk, _meta = data

        #         if isinstance(chunk, AIMessage):

        #             yield {"type":"token", "content" : chunk.text}

        #     elif mode == "updates" and isinstance(data, dict):
        #         interrupt = data.get("__interrupt__")
        #         if interrupt is not None:
        #             yield {"type": "interrupt", "content": interrupt}




    def __call__(self, prompt: str):

        yield from self._stream({'messages':[HumanMessage(content = prompt)]})

        
