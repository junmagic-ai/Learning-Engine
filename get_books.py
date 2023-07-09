# Search and download eBooks from Libgen 
# Need to git clone this: https://github.com/viown/libgen-dl

from libgenesis import Libgen
import asyncio, subprocess, os

from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import PyPDF2
import shutil

# Create libgen object
lg = Libgen(sort= 'year', sort_mode= 'DESC', result_limit= '1')

# Open the 'Booklist.txt' file
with open('Booklist.txt') as f:
    # Read the lines of the file into a list
    lines = f.readlines()

# Convert the list of lines into a list of book names
booklist = [line.strip() for line in lines]
print("Booklist is "+str(booklist)+'\n')

# for book in booklist 
#   while not chosen
#       keep showing the next available item 
#           if chosen, move to next book search
async def search():
    #bookMD5s = []

    for book in booklist: 
        # search for the book in libgen
        print("searching for..."+book+'\n')
        result = await lg.search(book)
        found = False
        for item in result: 
            if(result[item]['extension']=='epub'):
                print(result[item]['extension']+" | "+result[item]['year']+" | "+str(round(int(result[item]['filesize'])/1000000,1))+"MB | "+result[item]['title']+" | "+result[item]['language']+" | "+result[item]['author']+" | ")
                # ask the user if this is the one they want?
                while True:
                    user_input = input("This one? (Y/N) ")
                    if user_input == "Y" or user_input == "y":
                        found = True
                        #print (result[item]['md5'])
                        subprocess.call(["python","libgen-dl/libgen-dl.py", result[item]['md5']])
                        #os.system("move C:\\Users\\PlutoniaX\\Satoshi\\TLDR\\*.epub C:\\Users\\PlutoniaX\\Satoshi\\TLDR\\Books")
                        break
                    elif user_input == "N" or user_input == "n":
                        break
                    else: 
                        print("Invalid input. Please enter Y or N.")
                if found:
                    break

asyncio.run(search())

# move all epubs into Books folder 

# Create the 'Books' directory if it doesn't exist
if not os.path.exists('Books'):
    os.makedirs('Books')

# Iterate through the files in the current directory
for file in os.listdir():
    # Check if the file has a .epub or .pdf extension
    if file.endswith('.epub') or file.endswith('.pdf'):
        # Move the file to the 'Books' directory
        shutil.move(file, os.path.join('Books', file))


# Converts epubs to txt files
# Set the directory where the ePub files are located
input_dir = 'Books'
output_dir = "Texts"

# run through each file in input folder
for filename in os.listdir(input_dir):
    full_text = ""

    # for each epub file
    if filename.endswith('.epub'):

        # get book title and content
        book = epub.read_epub(os.path.join(input_dir, filename))
        book_title = book.get_metadata('DC', 'title')[0][0]
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                html_content = item.get_content().decode('utf-8')
                soup = BeautifulSoup(html_content, 'html.parser')  
                text = soup.get_text()
                full_text += text
        
        # write to a txt file named after the book title
        txt_title = f"{book_title}.txt"
        with open(os.path.join(output_dir, txt_title), 'w',encoding='utf-8') as f:
            f.write(full_text)
    
    # for each pdf file
    elif filename.endswith('.pdf'):
        pdf_file = open(os.path.join(input_dir, filename), 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            full_text += page_obj.extract_text()
        pdf_file.close()
        
        # write to a txt file named after the book title
        txt_title = f"{filename[:-4]}.txt"
        with open(os.path.join(output_dir, txt_title), 'w',encoding='utf-8') as f:
            f.write(full_text)