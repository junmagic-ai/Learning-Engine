import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

def gpt_summarise (chunk):
    openai.api_base = 'https://api.hypere.app'
    api_key = st.secrets["OPENAI_API_KEY"]
    docs = [Document(page_content=chunk)]
    
    llm=ChatOpenAI(openai_api_key=api_key, temperature=0,model_name="gpt-3.5-turbo")
    chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run (docs)
    
    return summary


def claude_summarise (chunk):
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

# open the file at the given filepath and return its content
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


if __name__ == '__main__':

    #set parameters
    input_directory = 'Texts'
    output_directory = 'Summaries'

    # loop through all files in folder
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        text = open_file(filepath)

        # break them down into chunks, 2000 characters each
        chunks = textwrap.wrap(text, 1400,break_long_words=False)
        count = 0
        index = 0

        print ("Summarising: "+ filename +"...\n")
        
        # loop over the chunks
        for chunk in chunks:

            # try generate a summary through all available bot instances
            count = count + 1
            success = False
            error_not_yet_shown = True
            retry_count = 0
            while not success:
                try:
                    summary = summarise(chunk)
                    summary = summary.replace("---", "\n- ")
                    success = True
                    retry_count = 0 
                except Exception as not_summarised:
                    print(not_summarised)
                    if error_not_yet_shown: 
                        print ("Hold tight, retrying until it works...\n")
                        error_not_yet_shown = False 
                    success = False
                    with open ('error_log.txt', 'w', encoding = 'utf-8') as f:
                        f.write ("Summarisation failed for: "+filename+" for the following chunk of text:\n\n\""+chunk+"\"\n\n")
                    f.close()
                    retry_count += 1
                if retry_count >= 5:
                    time.sleep(30)
                    retry_count = 0

            print('\n\n\n', count, 'of', len(chunks), ' - ', summary)

            # append to and save the summary file in the Summaries/ folder
            with open(os.path.join(output_directory, filename), 'a', encoding='utf-8') as f:
                f.write(summary + '\n\n')
            f.close()