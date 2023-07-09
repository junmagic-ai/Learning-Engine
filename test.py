# deploy a salient points generator

import streamlit as st 
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from io import StringIO

uploaded = st.file_uploader(label="Upload PDF, ePub or text files you want to summarise:",type=["pdf","epub","txt"],accept_multiple_files=True)

for file in uploaded: 
    st.write(file.getvalue().decode("utf-8"))
    data = UnstructuredPDFLoader(file)
    # st.write ("File Name is "+file.name)    
    # print (f'You have {len(data1)} document(s) in your data')
    # print (f'There are {len(data1[0].page_content)} characters in your document')    