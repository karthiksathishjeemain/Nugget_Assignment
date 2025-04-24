# Restaurant Knowledge Base RAG Project

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for restaurant information. It retrieves relevant restaurant data from a vector database in response to user queries and uses a large language model (LLM) to generate helpful, context-aware responses.

---

## Architecture

The system consists of the following components:

### Vector Database Pipeline

1. `href_collection.py` – URL Collection  
2. `data_collection.py` – Data Collection  
3. `data_cleaning.py` – Data Cleaning  
4. `store.py` – Vector Database Storage

### RAG System

- `llm_model.py` – LLM Model Integration  
- `tool_knowledge_base.py` – Knowledge Base Tool  
- `agent.py` – Agent Implementation  
- `system_message.py` – System Messaging  
- `app.py` – Web Interface  

---

## Setup and Installation

### Prerequisites

- Python 3.8+  
- Qdrant vector database access  
- Groq API key for LLM access  

### Environment Setup

1. Clone the repository
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file with the following variables:

    ```bash
    GROQ_API_KEY=your_groq_api_key_here
    QDRANT_URL=your_qdrant_url_here
    QDRANT_API_KEY=your_qdrant_api_key_here
    ```
4. Create a websites.txt file in vector_db folder and write down the restaurant urls line by line


---

## Data Pipeline

The data pipeline collects restaurant information from web sources and stores it in a Qdrant vector database:

1. Collect URLs from restaurant websites
2. Scrape content from each URL
3. Clean and structure the data
4. Generate embeddings and store in Qdrant

To run the full pipeline:

```bash
python vector_db/main.py
```
## RAG Implementation

The RAG system uses LangChain, LangGraph, and the Groq API to deliver restaurant information:

1. Queries are processed through the RAG agent
2. Relevant documents are retrieved from the knowledge base
3. The LLM generates responses based on retrieved context

## Web Interface

The application includes a Streamlit web interface:

```bash
 streamlit run app.py
```
Testing
Individual components can be tested using their respective main functions:
```bash
python llm_model.py  # Test the LLM integration
python tool_knowledge_base.py  # Test the knowledge base retrieval
python agent.py  # Test the RAG agent
```
## Project Structure
```bash
├── rag/
│   ├── agent.py          # RAG agent implementation
│   ├── app.py            # Streamlit web interface
│   ├── llm_model.py      # LLM wrapper for Groq
│   ├── system_message.py # System prompt messages
│   └── tool_knowledge_base.py # Knowledge base integration
├── vector_db/
│   ├── main.py           # Pipeline orchestration
│   ├── href_collection.py # URL collection
│   ├── data_collection.py # Data scraping
│   ├── data_cleaning.py   # Content processing
│   └── store.py          # Vector database operations
├── .env                  # API keys and credentials
├── .gitignore            # Git ignore file
├── requirements.txt      # Project dependencies
└── README.md             # This file
```
## Future Improvements
1. The while scraping the contents, use a image reading model as most of the menu section are in images for many restaurants
2. Replace the Llama model from Groq to Huggingface to remove the free token restrictions.

### Note:
If you change the collection name in `vector_db\store.py` then remember to change the collection name in `rag\tool_knowledge_base.py` as well at line number 43.

### References and help taken:
I have taken help from Langchain Docs and for generating Docstrings for each function,the data cleainng algorithm and README file and resolving errors while building the project, I have taken help from Claude LLM.