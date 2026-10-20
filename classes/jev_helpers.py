from langchain_typesafe import Score, Choice, Noul

class JevState:

    def __call__(self, state:str):

        self.state = {"state": state}


