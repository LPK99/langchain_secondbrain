import os
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def process_pdf_file(file, apikey):
    os.environ["OPENAI_API_KEY"] = apikey
    # location of the pdf file/files. 
    doc_reader = PdfReader(file)

    # read data from the file and put them into a variable called raw_text
    raw_text = ''
    for i, page in enumerate(doc_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    len(raw_text)
    raw_text[:100]

    # Splitting up the text into smaller chunks for indexing
    text_splitter = CharacterTextSplitter(        
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 200, #striding over the text
        length_function = len,
    )
    texts = text_splitter.split_text(raw_text)
    len(texts)

    # Download embeddings from OpenAI
    embeddings = OpenAIEmbeddings(openai_api_key=apikey)
    docsearch = FAISS.from_texts(texts, embeddings)
    docsearch.embedding_function

    # set up FAISS as a generic retriever 
    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":4})

    # create the chain to answer questions 
    rqa = RetrievalQA.from_chain_type(llm=OpenAI(), 
                                  chain_type="stuff", 
                                  retriever=retriever, 
                                  return_source_documents=True)
    return rqa

def query(question, file, apikey):
    query = question
    return process_pdf_file(file, apikey)(query)['result']