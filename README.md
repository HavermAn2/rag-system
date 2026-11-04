RAG System
This is my RAG (Retrieval-Augmented Generation) project that I am building with Python.

I started working on it because I wanted to understand how RAG systems actually work, not just follow tutorials. The main idea is to let users upload PDF documents and ask questions about their content using a local LLM.

The project is still in development. Some parts are already working, but there are also things I want to improve or completely change.
Technologies
- Python
- FastAPI
- Qdrant
- SentenceTransformers
- Ollama (Qwen3)
- Celery
- Redis
- PyMuPDF
- Docker
How it works
The system has two main processes: document processing and answering user questions.

When a user uploads a PDF file, the backend saves it locally and sends a task to Celery. The worker extracts text from the PDF, cleans it and splits into smaller chunks.

After that, each chunk is converted into an embedding using the multilingual-e5-base model. These embeddings are stored in Qdrant together with some metadata, like document name, page number and chunk index.

When a user asks a question, the system converts the question into an embedding and searches Qdrant for the most similar chunks.

The retrieved chunks are then sent to a local LLM through Ollama. The model uses this context to generate an answer.

I am trying to make the model answer only based on the uploaded documents, but there is still some work to do with the quality of retrieval and prompts.
Current features
- PDF uploading
- Text extraction and cleaning
- Text chunking with overlap
- Embedding generation
- Vector storage in Qdrant
- Semantic search
- Local LLM integration with Ollama
- Background document processing with Celery and Redis
- Document management through REST API
Project structure
I tried to separate different parts of the application instead of putting everything in one file.

FastAPI handles HTTP requests, services contain the main application logic, and Celery workers process more expensive tasks in background.

I also use dependency injection and FastAPI lifespan to manage shared resources like the Qdrant client and embedding model.

This architecture is probably not perfect, but it makes the code easier for me to understand and maintain.
What I learned
While building this project I got more experience with Python backend development, REST APIs and working with external services.

I also learned how vector databases work, how embeddings are used for semantic search and why background processing can be useful when working with large documents.

One of the harder parts was connecting FastAPI, Celery and Redis correctly, especially on Windows. I also had some problems with chunking and storing data in Qdrant.

Most of these problems helped me better understand how different parts of backend applications communicate with each other.
Plans
There are still several things I want to add or improve:
- Better chunking strategies
- Hybrid search (BM25 + vector search)
- Better document metadata and filtering
- Improved error handling
- Automated tests
- Simple frontend with React
- Docker Compose for easier setup
- Better LLM responses and prompt handling
- Performance optimization
About the project
This is a personal project that I develop while studying Computer Science.

My main goal is to improve my backend development skills and get more practical experience with AI technologies.

I don't want to just use ready-made RAG frameworks without understanding what happens inside, so I try to implement and connect most of the components myself.

The project is not finished yet, and I will continue improving it as I learn new things.
