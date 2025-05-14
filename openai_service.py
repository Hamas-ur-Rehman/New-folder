import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from vector_db import retriver
import logging
from mongo_service import save_chat, fetch_chat
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s - %(message)s'
)

def call_openai_api(question):
    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.environ.get("GEMINI_API_KEY")
    )
    response = client.chat.completions.create(
        temperature=0.7,
        model="gemini-2.0-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    print(response.choices[0].message.content)

def call_openai_api2(messages):
   
    response = ChatOpenAI(
        model="gemini-2.0-flash",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.environ.get("GEMINI_API_KEY")

    ).invoke(messages)

    return response


def call_llm(userid,question):
    messages = [
            SystemMessage(content="You are a helpful assistant."),
        ]

    messages.extend(fetch_chat(userid))

    try:
        logging.info(f"User question: {question}")
        data = retriver(question)
        messages.append(HumanMessage(content=data))
        messages.append(HumanMessage(content=question))
        response = call_openai_api2(messages)
        messages.append(response)


        save_chat({
            "userid": userid,
            "role": "user",
            "content": question
        })
        save_chat({
            "userid": userid,
            "role": "assistant",
            "content": response.content
        })
        return response.content
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# print(call_llm("asdjgasdgj","What is hydrogen fuel?"))
# print(call_llm("asdjgasdgj","what was my first question?"))


