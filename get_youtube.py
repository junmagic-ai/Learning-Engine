import yt_dlp
import os
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube


def get_youtube(url):
    transcript = ""
    output_dir = "Texts"
    if "watch?v=" in url:
        video = YouTube(url)
    elif "youtu.be" in url:
        v_id = url.split("/")[-1]
        video = YouTube("https://youtube.com/watch?v="+v_id)
    else:
        print("Invalid YouTube URL")
    srt = YouTubeTranscriptApi.get_transcript(video.video_id)
    if (srt):
        for item in srt:
            transcript = transcript+(item['text'])+" "
        print (transcript)
        ydl_opts = {
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info['title']

        with open(os.path.join(output_dir, f'{video_title}.txt'), 'w', encoding='utf-8') as f:
            f.write(transcript)
    else: 
        download_mp3 (url)


def download_mp3(url):
    mp3_dir = 'Audio\\'
    # Fetch video metadata
    ydl_opts = {
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info['title']
        print ('video title is..'+video_title)

    # Sanitize the video title to create a valid filename
    filename = "".join([c for c in video_title if c.isalnum() or c in (' ', '.', '-', '_')]).rstrip()
    path = os.path.abspath(mp3_dir + filename + '.mp3')

    if os.path.exists(path):
        return path

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{mp3_dir}{filename}.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return os.path.abspath(mp3_dir + filename + '.mp3')


video_url = "https://www.youtube.com/watch?v=O-e5nnYKSYw"
get_youtube(video_url)
