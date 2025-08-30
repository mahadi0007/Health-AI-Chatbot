import os
import cohere
import openai
from dotenv import load_dotenv
from document_processor import load_and_chunk_documents

# --- 1. INITIAL SETUP ---
# Load environment variables from .env file
load_dotenv()

# Get API keys from environment
cohere_api_key = os.getenv("COHERE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if keys are available
if not cohere_api_key or not openai_api_key:
    raise ValueError("API keys for Cohere or OpenAI not found in .env file.")

# Initialize the Cohere and OpenAI clients
co = cohere.Client(cohere_api_key)
openai.api_key = openai_api_key

# --- 2. IN-MEMORY VECTOR STORE ---
# In a real application, we would use a dedicated vector database.
# For this exercise, we'll store vectors in a simple list.
vector_store = []


def build_vector_store():
    """
    Loads documents, creates embeddings, and stores them in the in-memory vector store.
    This function should be run once when the application starts.
    """
    global vector_store
    print("Building vector store...")

    # We use the function from our previous step
    chunks = load_and_chunk_documents()

    # Get the text content from each chunk
    chunk_texts = [chunk.page_content for chunk in chunks]

    # Generate embeddings for the chunks using Cohere
    response = co.embed(
        texts=chunk_texts, model="embed-english-v3.0", input_type="search_document"
    )
    embeddings = response.embeddings

    # Store the original text and its embedding together
    vector_store = [
        {"text": text, "embedding": emb} for text, emb in zip(chunk_texts, embeddings)
    ]

    print(f"Vector store built successfully with {len(vector_store)} vectors.")
    # The vector_store now contains our document knowledge base


# --- 3. RAG QUERY FUNCTION ---
def query_rag(query: str):
    """
    Takes a user query and returns a generated answer from the RAG pipeline.
    """
    print(f"\nReceived query: '{query}'")

    # Embed the user's query
    query_embedding_response = co.embed(
        texts=[query], model="embed-english-v3.0", input_type="search_query"
    )
    query_embedding = query_embedding_response.embeddings[0]

    # Prepare documents as a simple list of strings
    retrieved_docs = [item["text"] for item in vector_store]

    # Rerank the retrieved documents for better relevance
    print("Reranking documents...")
    rerank_response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=retrieved_docs,  # We now send the simple list of strings
        top_n=3,
    )

    # Build context using the index from the reranker's results
    reranked_docs_text = []
    for result in rerank_response.results:
        # The reranker gives us the index of the best matching document
        doc_index = result.index
        # We use that index to get the text from our original list
        reranked_docs_text.append(retrieved_docs[doc_index])

    context = "\n\n---\n\n".join(reranked_docs_text)

    print(f"\n--- Context Sent to LLM ---\n{context}\n---------------------------\n")

    # Generate an answer using the LLM with the context
    print("Generating answer...")
    prompt = f"""
    You are a helpful assistant. Use the following context to answer the user's question.
    If the answer is not found in the context, say "I don't have enough information to answer that."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    # Build the vector store first
    build_vector_store()

    # Ask a sample question
    test_query = "What are the benefits of cardio?"
    answer = query_rag(test_query)

    print("\n--- FINAL ANSWER ---")
    print(answer)
    print("--------------------")
