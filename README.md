# Learning-Engine

Using OpenAI's Whisper to transcribe Apple Podcasts and Youtube Videos into text, then using GPT 3.5 Turbo 16k to extract insights, principles, recommendations, predictions and key examples from the text into a CSV file for easy viewing. 

## How to use

1. Install python
2. Open Terminal (Mac) or Command Prompt (Win) and run:
   ```pip install -r requirements.txt```
4. Put your OpenAI API key in api_key.txt
5. Put the URLs of the Apple Podcasts and / or Youtube videos in input.txt
6. Run main.py in Terminal / Command Prompt:
   ```python main.py```
7. Wait a while... and the gems will be saved in Final_Gems.csv
