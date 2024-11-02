from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from prompt_templates import chat_template
from agent import query_engine
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

from users.controller import User

load_dotenv()

Settings.llm = OpenAI(temperature=0.2, model="gpt-4o")
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    q: str
    user_id: int


@app.post("/chat")
async def ask(query: Query):
    user = User()
    # user.clear_chat_history(query.user_id)
    chat_history = user.get_chat_history(query.user_id)
    formatted_query = chat_template.format(user_query=query.q, history=chat_history)
    response = query_engine.query(formatted_query)
    return {"response": response.response}
