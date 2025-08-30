This project is a complete, end-to-end Retrieval-Augmented Generation (RAG) chatbot application. It uses a Python/FastAPI backend and a Next.js/ShadCN frontend.

---

## Chosen Topic and Document Sources

*   **Topic:** The Benefits of Regular Exercise
*   **Document Source:** A custom-generated text document (`exercise_benefits.txt`) covering the basics of cardiovascular, strength, and mental health benefits of exercise.

---

## Setup and Running the Application

### Prerequisites
*   Python 3.8+
*   Node.js and npm
*   An OpenAI API Key
*   A Cohere API Key

### 1. Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the `backend` directory and add your API keys:
    ```
    OPENAI_API_KEY="your-openai-key-here"
    COHERE_API_KEY="your-cohere-key-here"
    ```
5.  Run the backend server:
    ```bash
    uvicorn main:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

### 2. Frontend Setup

1.  In a separate terminal, navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install the required Node.js packages:
    ```bash
    npm install
    ```
3.  Run the frontend development server:
    ```bash
    npm run dev
    ```
    The frontend will be running at `http://localhost:3000`.

---

## Assumptions and Trade-offs

*   **Vector Store:** For simplicity and to meet the project requirements, an in-memory list is used as the vector store. This is efficient for a small number of documents but would be replaced by a dedicated vector database (like Pinecone, Weaviate, or ChromaDB) in a production environment for scalability and persistence.
*   **Error Handling:** Basic error handling is implemented for the API call on the frontend. A production system would have more comprehensive logging and error-handling strategies on both the frontend and backend.
*   **Security:** CORS is enabled for all origins (`"*"`) for ease of development. In a production environment, this would be restricted to the specific frontend domain.
