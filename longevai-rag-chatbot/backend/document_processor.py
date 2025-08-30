import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define the path for the data directory
DATA_PATH = "data/"


def load_and_chunk_documents():
    """
    Loads documents from the data path and splits them into smaller chunks.

    Returns:
        list: A list of document chunks.
    """
    print("Loading and chunking documents...")

    # Check if the data file exists
    file_path = os.path.join(DATA_PATH, "exercise_benefits.txt")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file was not found at path: {file_path}")

    # Load the document
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    # Initialize the text splitter
    # chunk_size: The maximum number of characters in a chunk.
    # chunk_overlap: The number of characters to overlap between chunks to maintain context.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)

    # Split the documents into chunks
    chunked_documents = text_splitter.split_documents(documents)

    print(f"Successfully created {len(chunked_documents)} chunks.")
    return chunked_documents


# This block allows us to test the function directly
# It will only run when you execute this file with "python document_processor.py"
if __name__ == "__main__":
    chunks = load_and_chunk_documents()

    # Print the content of the first chunk to see what it looks like
    print("\n--- Sample Chunk 1 ---")
    print(chunks[0].page_content)
    print("------------------------")
