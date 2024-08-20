from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from dotenv import load_dotenv
from prompts import system_prompt
import pandas as pd
import json
import pygame
from data_prepration import data_creation,getting_values
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
import time
import asyncio
load_dotenv()
# from main import Groq
#from WEBUI import GROQ_API_KEY


class Getting_response:
    def __init__(self,model) -> None:
        self.model = model
        self.llm = ChatGroq(temperature=0, model_name=self.model, groq_api_key=os.getenv("GROQ_API_KEY"))
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{text}")
            ])
        self.conversation = LLMChain(
                llm=self.llm,
                prompt=self.prompt,
                memory=self.memory
            )
            
    async def process(self, text):
        self.memory.chat_memory.add_user_message(text)
        start_time = time.time()
        response = await asyncio.to_thread(self.conversation.invoke, {"text": text})
        end_time = time.time()
        self.memory.chat_memory.add_ai_message(response['text'])
        elapsed_time = int((end_time - start_time) * 1000)
        print(f"LLM ({elapsed_time}ms): {response['text']}")
        return response['text']
        
            
if __name__ == "__main__":
        pass