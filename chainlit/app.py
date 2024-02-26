import llm_commons.proxy.base
from llm_commons.proxy.openai import Completion
from llm_commons.proxy.identity import AICoreProxyClient
from llm_commons.langchain.proxy import ChatOpenAI
from llm_commons.btp_llm.identity import BTPProxyClient
from llm_commons.langchain.proxy import init_llm, init_embedding_model

llm_commons.proxy.base.proxy_version = 'aicore'
aic_proxy_client = AICoreProxyClient()
# btp_proxy_client = BTPProxyClient()

from llm_commons.proxy.base import set_proxy_version
set_proxy_version('aicore') # for an AI Core proxy
llm_4 = ChatOpenAI(proxy_model_name='gpt-4')
# chat.predict("What is the world's best company to work?")


from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.agents import initialize_agent, AgentType
from langchain.tools.tavily_search import TavilySearchResults


""" # set up the agent
llm = llm_4
search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search)

# initialize the agent
agent_chain = initialize_agent(
    [tavily_tool],
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
) """

# run the agent
#agent_chain.run(
#    "1981年12月17日出生的人运势分析",
#)


""" from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    model = llm_4
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send() """

# from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.chains import LLMChain

import chainlit as cl


""" @cl.on_chat_start
async def on_chat_start():
    model = llm_4
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
            ),
            ("human", "{question}"),
        ]
    )
    chain = agent_chain

    cl.user_session.set("chain", chain)


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")  # type: LLMChain

    res = await chain.arun(
        question=message.content, callbacks=[cl.LangchainCallbackHandler()]
    )

    await cl.Message(content=res).send() """


@cl.on_chat_start
def start():
    llm = llm_4
    search = TavilySearchAPIWrapper()
    tavily_tool = TavilySearchResults(api_wrapper=search)

# initialize the agent
    agent = initialize_agent(
    [tavily_tool],
    llm,
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
