from langchain_typesafe import Choice, TypeSafeClassifier, Noul

from classes.jev_helpers import JevState




class JevToolAgent: 

    def __init__(self, state: JevState, tool_options: list[str], history: list[dict], latest_prompt: str):

        self.state = state

        self.tool_options = tool_options

        self.history = history

        self.latest_prompt = latest_prompt


    def __call__(self) -> tuple:

        classifier = TypeSafeClassifier()

        response = classifier.invoke({

            "state" : f"The converations so far is {self.history}, the user has followed up with {self.latest_prompt}" ,

            "questions" : {

                "tool_required" : Noul(instructions= "Is a tool required to satisy this prompt? "),

                "tools" : Choice(

                    instructions = "Select the most relevant tool for this task", 

                    criteria = {tool: tool for tool in self.tool_options}


                )
                }

        })

        return (response.nouls['tool_required'].noul, response.choices['tools'].choice)


class JevMemoryAgent:

    def __init__(self, memory: list):

        self.memory = memory




