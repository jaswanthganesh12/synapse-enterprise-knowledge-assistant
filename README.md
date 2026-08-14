# Synapse

Synapse is an enterprise knowledge assistant that lets users upload documents and ask questions using natural language.

It combines hybrid search, vector embeddings, reranking, and grounded LLM responses to retrieve relevant information and provide source citations.

## Features

- JWT authentication and role-based access control
- PDF, TXT, and Markdown document ingestion
- Automatic document parsing and chunking
- PostgreSQL for document and chunk storage
- Qdrant for vector search
- BM25 + dense vector hybrid retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-encoder reranking
- Conversation history
- Grounded Gemini responses
- Source citations for retrieved information
- Retrieval and latency evaluation
- 10,000-document scalability benchmark

## Architecture

```text
Documents
    ↓
Parser Registry
    ↓
Chunking
    ↓
PostgreSQL ────────┐
                   ↓
               Embeddings
                   ↓
                 Qdrant
                   ↓
        ┌──────────┴──────────┐
        ↓                     ↓
   BM25 Search          Vector Search
        └──────────┬──────────┘
                   ↓
                  RRF
                   ↓
               Reranking
                   ↓
            Retrieved Context
                   ↓
              Gemini LLM
                   ↓
          Answer + Citations
