from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def handle_pdf(file_path="./HydrogenFuel.pdf", chunk_size=500):
    loader = PyPDFLoader(file_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )

    docs = loader.load()

    chunks = []

    for i in docs:
        text = i.page_content
        peices = text_splitter.split_text(text)
        chunks.extend(peices)

    return chunks