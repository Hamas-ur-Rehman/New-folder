from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pdf_handler import handle_pdf
from dotenv import load_dotenv
import logging
load_dotenv()

def loader():
    embeddings = OpenAIEmbeddings()

    vector_db = Chroma(
        persist_directory="./vector_db",
        embedding_function=embeddings,
        collection_name="hydrogen_fuel"
    )

    logging.info("Loading PDF...")
    chunks = handle_pdf()
    logging.info("Adding texts to vector_db...")
    Chroma.add_texts(vector_db, chunks)
    logging.info("Done.")


def retriver(question):
    embeddings = OpenAIEmbeddings()

    vector_db = Chroma(
        persist_directory="./vector_db",
        embedding_function=embeddings,
        collection_name="hydrogen_fuel"
    )

    logging.info("Retrieving...")
    docs = vector_db.similarity_search(question, k=3)

    data = []

    for i in docs:
        text = i.page_content
        data.append(text)
    return "\n".join(data)

# loader()
# logging.info(retriver("What is hydrogen fuel?"))