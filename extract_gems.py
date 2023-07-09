import openai
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
import re
from utils import open_file

def old_extract_gems_from (chunk):
    api_key = "1G7BJRYGLDGz1_YAL2Agc93zyx0Dl_pe2xIybgAHUk8"
    openai.api_base = "https://chimeragpt.adventblocks.cc/v1"
    docs = [Document(page_content=chunk)]
    
    prompt_template = """Synthesise the following TEXT and extract key 
    insights, principles, recommendations, predictions and key examples. Label each insight, principle, recommendation, prediction and key example with the right label. 
    For example if the text is an idea, label it as "[idea] text", if the text is a key example, label it as "[key example] text", and so on.\n'
    
    TEXT:
    {text}
    """

    PROMPT = PromptTemplate(template = prompt_template,input_variables = ["text"])
    llm=OpenAI(openai_api_key=api_key, temperature=0,model_name="claude-instant-100k")
    chain = load_summarize_chain(llm, chain_type="stuff",prompt = PROMPT)
    gems  = chain.run (docs)
    return gems


def extract_gems_from(chunk):
    openai.api_key = "1G7BJRYGLDGz1_YAL2Agc93zyx0Dl_pe2xIybgAHUk8"
    openai.api_base = "https://chimeragpt.adventblocks.cc/v1"

    prompt_txt = """Synthesise the following TEXT and extract key 
    insights, principles, recommendations, predictions and key examples. Label each insight, principle, recommendation, prediction and key example with the right label. 
    For example if the text is an idea, label it as "[idea] text", if the text is a key example, label it as "[key example] text", and so on.\n'
    
    TEXT:\n
    """+chunk
   
    response = openai.ChatCompletion.create(
        model='claude-instant-100k',
        messages=[
            {'role': 'user', 'content': prompt_txt},
        ]   
    )

    return response["choices"][0]["message"]["content"]

folder = 'Gems'

# Regular expression to match the labels
label_pattern = re.compile(r'\[(idea|principle|key example|prediction|insight|recommendation)\]', re.IGNORECASE)

# Function to extract lines with labels
def extract_lines_with_labels(text):
    lines = text.splitlines()
    extracted_lines = []
    
    for line in lines:
        match = label_pattern.search(line)
        if match:
            category = match.group(1).lower()
            text = label_pattern.sub('', line).strip()
            extracted_lines.append((category, text))
    
    return extracted_lines

