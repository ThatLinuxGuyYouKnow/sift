from uuid import uuid4



def handlePrompt(thread_id : str | None, user_prompt : str):


    if not thread_id: thread_id = str(uuid4())