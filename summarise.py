import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

def gpt3_completion (chunk):
    openai.api_base = 'https://api.hypere.app'
    api_key = st.secrets["OPENAI_API_KEY"]
    docs = [Document(page_content=chunk)]
    
    llm=ChatOpenAI(openai_api_key=api_key, temperature=0,model_name="gpt-3.5-turbo")
    chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run (docs)

    return summary

def claude (chunk):
    api_key = st.secrets["CLAUDE_API_KEY"]
    openai.api_base = "https://chimeragpt.adventblocks.cc/v1"
    docs = [Document(page_content=chunk)]
    
    prompt_template = """Please provide a summary of the following text.
    Please provide your output in a manner that only contains the key points and nothing else - no statements like 'Here are the key points summarized from the text:' or 'Let me know if you need any clarification or have additional questions.'
    TEXT:
    {text}
    Here are the key points from the text: """

    PROMPT = PromptTemplate(template = prompt_template,input_variables = ["text"])
    llm=ChatOpenAI(openai_api_key=api_key, temperature=0,model_name="claude-instant-100k")
    chain = load_summarize_chain(llm, chain_type="stuff",prompt = PROMPT)
    summary = chain.run (docs)
    
    st.write(f'{summary}')
    return summary