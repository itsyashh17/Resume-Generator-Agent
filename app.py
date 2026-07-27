import streamlit as st
from IPython.core.prefilter import PythonOpsChecker
import os
import time
import langchain
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tavily import TavilyClient
import pytesseract as pyt
import numpy as np
from langchain.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent

#===================================FRONTEND============================
st.title("AI Resume Generator")

GOOGLE_API_KEY=st.sidebar.text_input("Google Api Key",type='Password')
GROQ_API_KEY=st.sidebar.text_input("GROQ Api Key",type='password')
TAVILY_API_KEY=st.sidebar.text_input("TAVILY Api Key",type='password')

if not GOOGLE_API_KEY:
  st.warning("Provide Google Api Key")

#==============================Model and Agent Code===========================
#tool 1
def search_latest_news_jobs(query):
  """This function helps to get
  latest news or latest jobs
  related to user given query
  using tavily"""

  from tavily import TavilyClient
  client= TavilyClient(api_key = Tavily_API_Key)
  return client.search(query)

  #Step 4:Model and Agent Creation
model1=ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY
)

model2=ChatGroq(
    model="qwen/qwen3.6-27b",
    api_key= GROQ_API_KEY
)

#============================Agent With Tool========================
agent=create_agent(
    model=model1,  #can be model2 also
    tools=[search_latest_news_jobs]

)

#Let's generate prompt for resume using model

def prompt_generator():
  prompt="""YOu aare a helpful AI resume
  maker,I want you to use chain-of-thoughts
  and give detailed prompt for model
  where user want to generate resume
  for fresher or experienced one
  in HTML format,you have to give proper
  set of instructions,and make sure to keep
  design professional"""

  response = model1.invoke(prompt)
  prompt_ans = response.content[-1]['text']
  #print(prompt_ans)

  file_name='prompt.txt'
  with open(file_name,'w') as f:
    f.write(prompt_ans)

  print('Prompt file generated sucessfully!!')

  prompt_generator(_)


  #final_agent
#tool 2
def prompt_reader():
  with open('prompt.txt','r') as f:
    prompt=f.read()
  return prompt

prompt="""I want complete profesional
resume with dynamic design using advance High CSS and JS
with attractive interface
and must how user input details

System Instructions:Only Give HTML Code as output"""

final_prompt = prompt_reader()

url="https://th.bing.com/th/id/OIP.eX8OBnkIRP5kR6GxlsJXWwHaJQ?w=147&h=185&c=7&r=0&o=7&pid=1.7&rm=3"
#change this when required new reume by user,pass details
user_info=st.text_input("Give Your information: ")
user_photo=st.sidebar.file_uploader("Upload pic",type='image/jpeg')

user_query=f"""Give resume for python Devloper.
user details: {user_info}
use user profile image from given {user_photo}"""
final_query = final_prompt + user_query

if st.button("Generate Resume"):
  with st.spinner("Agent Creating Resume..."):

   response = agent.invoke({'messages':[{'role':'user',"content":final_query}]})
   code = response['messages'][-1].content[-1]['text']

   st.html(code, width="stretch",unsafe_allow_javascript=True)
   

