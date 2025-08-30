from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import build_vector_store, query_rag

# --- 1. APP INITIALIZATION ---

# Create the FastAPI app instance
app = FastAPI(
    title="RAG Chatbot",
    description="A simple RAG chatbot using FastAPI, Cohere, and OpenAI.",
    version="1.0.0",
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows our frontend (running on a different port) to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.).
    allow_headers=["*"],  # Allows all headers.
)

# --- 2. STARTUP EVENT ---


@app.on_event("startup")
def on_startup():
    """
    This function will be called once when the application starts.
    We build the vector store here to avoid rebuilding it for every request.
    """
    build_vector_store()


# --- 3. API DATA MODELS ---


# Pydantic model for the request body of our /query endpoint
class QueryRequest(BaseModel):
    query: str


# Pydantic model for the response body of our /query endpoint
class QueryResponse(BaseModel):
    answer: str


# --- 4. API ENDPOINT ---


@app.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    """
    The main endpoint to handle user queries.
    It takes a query and returns the RAG-generated answer.
    """
    # The 'request' object contains the JSON sent by the frontend
    user_query = request.query

    # Call our existing RAG pipeline function
    answer = query_rag(user_query)

    # Return the answer in the format defined by QueryResponse
    return {"answer": answer}
