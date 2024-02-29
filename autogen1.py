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

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

# user_proxy= autogen.UserProxyAgent(
#     name="user_proxy",
#     max_consecutive_auto_reply=10,
#     human_input_mode="NEVER",
#     llm_config=llm_config,
#        code_execution_config={
#         "use_docker": False,
#     },
# )


# user_proxy.initiate_chat(
#     assistant,
#     message="""what is the whether in shanghai?""",
# )

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "web",
        "use_docker": True,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
)

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant,
    #token可以从https://developer.microsoft.com/en-us/graph/graph-explorer获取
    # message="""请总结网页https://goodworkaround.com/2020/09/14/easiest-ways-to-get-an-access-token-to-the-microsoft-graph/上的内容， 将总结结果发送给kylino@hotmail.com. 请使用graph api来发送，所需token请查询变量{GRAPH_TOKEN}""", 
    message="""上海现在几点？""",
)

