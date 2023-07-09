# Main function calls all the other scripts to transcribes and process the URLs in input.txt

from get_apple_pod import download_apple_podcast 
from check_inputs import identify_url_type
import os, textwrap,csv
from transcribe_audio import transcribe
from utils import open_file
from extract_gems import extract_gems_from, extract_lines_with_labels

if __name__ == '__main__':

    # 1. Get URLs of Apple podcasts or Youtube videos from input.txt
    with open('input.txt', 'r') as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls]

    # 2. Check each URL's type to determine processing method
    for url in urls:
        url_type = identify_url_type(url)

        if (url_type == "Apple"): 
            download_apple_podcast(url)
        if (url_type =="Youtube"):
            print("youtube")

    # 3. If audio, transcribe them, save in folder named "Texts" and then delete the audio files
    if not os.path.exists("Audio"):
        os.makedirs("Audio")
    folder_to_transcribe = "Audio"
    for file_name in os.listdir(folder_to_transcribe):
        file_path = os.path.join(folder_to_transcribe, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('.m4a', '.mp3')):
            title, _ = os.path.splitext(file_name)
            transcribe(file_path, title)
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    
    # 4. Go through each text file and extract gems from it
    if not os.path.exists("Gems"):
        os.makedirs("Gems")
    folder_to_process = "Texts"
    gems_folder = 'Gems'
    for file_name in os.listdir(folder_to_process):
        all_gems =""
        file_path = os.path.join(folder_to_process, file_name)
        text = open_file(file_path)
        chunks = textwrap.wrap(text, 10000,break_long_words=False)
        for chunk in chunks:
            gems = extract_gems_from (chunk)
            all_gems += "\n".join(gems.splitlines())+ '\n\n'

        with open(os.path.join(gems_folder, f"{file_name}"), "w",encoding='utf-8') as f:
            f.write(all_gems)
        f.close()

    result_file = "Final_Gems.csv"
    # 5. Save the gems into the csv file
    with open(result_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Source", "Category", "Text"])

        for filename in os.listdir(gems_folder):
            file_path = os.path.join(gems_folder, filename)

            if os.path.isfile(file_path) and file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()

                extracted_lines = extract_lines_with_labels(text)
                
                for category, text in extracted_lines:
                    csv_writer.writerow([filename, category, text])
                    print(f"Gems saved. Shutting down...")