import openai
import re

def extract_gems_from(chunk):

    with open('api_key.txt', 'r') as f:
        openai.api_key = f.readline().strip()

    prompt_txt = """Synthesise the following TEXT and extract key 
    insights, principles, recommendations, predictions and key examples. Label each insight, principle, recommendation, prediction and key example with the right label. 
    For example if the text is an idea, label it as "[idea] text", if the text is a key example, label it as "[key example] text", and so on.\n'
    
    TEXT:\n
    """+chunk
   
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
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

