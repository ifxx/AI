# from ipywidgets import widgets
import json
import os
import requests
import llm_commons.proxy.base
from llm_commons.proxy.openai import Completion
from llm_commons.proxy.identity import AICoreProxyClient
from llm_commons.langchain.proxy import ChatOpenAI
from llm_commons.btp_llm.identity import BTPProxyClient
from llm_commons.langchain.proxy import init_llm, init_embedding_model
import autogen

llm_commons.proxy.base.proxy_version = 'aicore'

# resource_group = widgets.Text(
#     value='default', # resource group
#     placeholder='Resource group of deployments',
#     description='',
#     disabled=False
# )

# with open('config/irpa-d26-genaixl-cx-sec-cn-sk.json') as f: use path in container
with open('/home/autogen/autogen/myapp/irpa-d26-genaixl-cx-sec-cn-sk.json') as f:
    sk = json.load(f)

os.environ['AICORE_LLM_AUTH_URL'] = sk['url']+"/oauth/token"
os.environ['AICORE_LLM_CLIENT_ID'] = sk['clientid']
os.environ['AICORE_LLM_CLIENT_SECRET'] = sk['clientsecret']
os.environ['AICORE_LLM_API_BASE'] = sk["serviceurls"]["AI_API_URL"]+ "/v2"
# os.environ['AICORE_LLM_RESOURCE_GROUP'] = resource_group.value
os.environ['LLM_COMMONS_PROXY'] = 'aicore'
os.environ['ENDPOINT_URL'] = sk['endpoint']
os.environ['GRAPH_TOKEN'] = sk['graphToken']

llm_commons.proxy.resource_group = 'default'
llm_commons.proxy.api_base = os.environ['AICORE_LLM_API_BASE']
llm_commons.proxy.auth_url = os.environ['AICORE_LLM_AUTH_URL']
llm_commons.proxy.client_id = os.environ['AICORE_LLM_CLIENT_ID']
llm_commons.proxy.client_secret = os.environ['AICORE_LLM_CLIENT_SECRET']
llm_commons.proxy.endpoint_url = os.environ['ENDPOINT_URL']

aic_proxy_client = AICoreProxyClient()

response = requests.post(
        f'{os.environ["AICORE_LLM_AUTH_URL"]}/oauth/token',
        data={"grant_type": "client_credentials"},
        auth=(os.environ['AICORE_LLM_CLIENT_ID'], os.environ['AICORE_LLM_CLIENT_SECRET']),
        timeout=8000,
)
auth_token = response.json()["access_token"]

graph_token = os.environ['GRAPH_TOKEN']


llm_config={
    "config_list":[
        {
            # "base_url":"is the same with restful api url api_key is the restful api auth token"
            "base_url":llm_commons.proxy.endpoint_url,
            "api_key": auth_token,
            "api_version":"2023-05-15",
            "api_type":"azure"

        }
    ],
    "temperature": 0,
    "model":"gpt-4"
}



user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": True,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="TERMINATE",
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in compare and summarize.",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=22)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager, message="上海明天"
)