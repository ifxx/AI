from ipywidgets import widgets
import json
import os
import llm_commons.proxy.base
from llm_commons.proxy.openai import Completion
from llm_commons.proxy.identity import AICoreProxyClient
from llm_commons.langchain.proxy import ChatOpenAI
from llm_commons.langchain.proxy import init_llm, init_embedding_model
with open('C:\AI\AI\config\irpa-d26-genaixl-cx-sec-cn-sk.json') as f:
    sk = json.load(f)
os.environ['AICORE_LLM_AUTH_URL'] = sk['url']+"/oauth/token"
os.environ['AICORE_LLM_CLIENT_ID'] = sk['clientid']
os.environ['AICORE_LLM_CLIENT_SECRET'] = sk['clientsecret']
os.environ['AICORE_LLM_API_BASE'] = sk["serviceurls"]["AI_API_URL"]+ "/v2"
# os.environ['AICORE_LLM_RESOURCE_GROUP'] = resource_group.value
os.environ['LLM_COMMONS_PROXY'] = 'aicore'
os.environ['TAVILY_API_KEY'] = sk['tavily']

os.environ["BING_SUBSCRIPTION_KEY"] = sk['bing']
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

os.environ["CLIENT_ID"] = sk['azureClientId']
os.environ["CLIENT_SECRET"] = sk['azureClientSecret']


# llm_commons.proxy.resource_group = os.environ['AICORE_LLM_RESOURCE_GROUP']
llm_commons.proxy.api_base = os.environ['AICORE_LLM_API_BASE']
llm_commons.proxy.auth_url = os.environ['AICORE_LLM_AUTH_URL']
llm_commons.proxy.client_id = os.environ['AICORE_LLM_CLIENT_ID']
llm_commons.proxy.client_secret = os.environ['AICORE_LLM_CLIENT_SECRET']

from llm_commons.proxy.base import set_proxy_version
set_proxy_version('aicore') # for an AI Core proxy
from llm_commons.langchain.proxy import ChatOpenAI

llm_4 = ChatOpenAI(proxy_model_name='gpt-4-32k')
# chat.predict("What is the world's best company to work?")

from langchain_community.agent_toolkits import O365Toolkit

toolkit = O365Toolkit()
tools = toolkit.get_tools()

from langchain.agents import initialize_agent, AgentType, load_tools
# from langchain_community.utilities import BingSearchAPIWrapper


# from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.chains import LLMChain

import chainlit as cl


@cl.on_chat_start
def start():
    llm = llm_4
# initialize the agent
    agent = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    )

    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    res = await agent.arun(
        message.content, callbacks=[cl.AsyncLangchainCallbackHandler()]
    )

    await cl.Message(content=res).send()



# set up the agent
