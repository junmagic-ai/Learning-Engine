import re

def identify_url_type(url):
    youtube_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'
    spotify_pattern = r'(https?://)?(www\.)?open\.spotify\.com/episode/.+'
    apple_pattern = r'(https?://)?(www\.)?podcasts\.apple\.com/.+/podcast/.+'

    if re.match(youtube_pattern, url):
        return 'YouTube'
    elif re.match(spotify_pattern, url):
        return 'Spotify'
    elif re.match(apple_pattern, url):
        return 'Apple'
    else:
        return 'Unknown'
