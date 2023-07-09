# Some useful utility functions.. Not all are used...

from PyPDF2 import PdfReader
import textwrap, ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import textwrap, ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8',errors='replace') as infile:
        return infile.read()
def chunk_text(text,char):
    chunks = textwrap.wrap(text, width=char, break_long_words=False)
    return chunks

def convert_to_txt (file,file_ext):
    full_text=""
    if file_ext == ".epub":
        try:
            book = epub.read_epub(file)
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    html_content = item.get_content().decode('utf-8')
                    soup = BeautifulSoup(html_content, 'html.parser')  
                    text = soup.get_text()
                    full_text += text
        except Exception as oops:
            print("Something wrong with the file - could be corrupt, encrypted, or wrong format. Error: "+str(oops))
    elif file_ext == ".pdf":
        try:
            pdf = PdfReader(file)
            for page in pdf.pages:
                full_text+=page.extract_text()+" "
        except Exception as oops:
            print("Something wrong with the file - could be corrupt, encrypted, or wrong format. Error: "+str(oops))
    else:
        full_text=file.read()
    return full_text

def get_transcript(url):
    transcript=""
    go_ahead = False
    if "watch?v=" in url:
        video = YouTube(url)
        go_ahead = True
    elif "youtu.be" in url:
        v_id = url.split("/")[-1]
        video = YouTube("https://youtube.com/watch?v="+v_id)
        go_ahead = True
    else:
        print("Invalid YouTube URL")
        transcript = "Error"
    if(go_ahead):
        try:
            srt = YouTubeTranscriptApi.get_transcript(video.video_id)
            for item in srt:
                transcript = transcript+(item['text'])+" "
        except Exception as e:
            print("Error loading transcript - it doesn't exist or is not in English. Try another video.")
    
    return transcript