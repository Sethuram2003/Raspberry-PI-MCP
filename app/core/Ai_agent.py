import asyncio
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
import sys

from app.core.prompt import SYSTEM_PROMPT

load_dotenv()

checkpointer = InMemorySaver()

config = {
    "configurable": {
        "thread_id": "1"  
    }
}

def find_python_path():
    """Find Python binary path with packages"""
    return sys.executable 

python_executable = find_python_path()
current_dir = os.path.dirname(os.path.abspath(__file__))


async def chat_agent():
    llm = ChatOllama(model="kimi-k2:1t-cloud", temperature=0)

    McpConfig={}

    client = MultiServerMCPClient(McpConfig)
    tools = await client.get_tools()

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
    )

    return agent


async def main():
    agent = await chat_agent()

    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "tell me how did the agent perform in the conversation?"}
        ]
    }, config)

    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())