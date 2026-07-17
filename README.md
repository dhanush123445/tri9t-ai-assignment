# TRI9T AI Assignment

## Overview

This project is a FastAPI-based backend application that parses PDF documents into a hierarchical tree structure, supports document versioning, allows searching and node selection, generates AI-powered test cases using Groq Llama 3.3, and compares different versions of a document.

---

# Features

- PDF document upload
- Automatic document versioning
- Hierarchical tree parsing
- OCR fallback for scanned PDFs
- Table extraction
- Search document headings and content
- Save and retrieve node selections
- AI-generated test cases using Groq Llama 3.3
- Compare different document versions

---

# Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- PyMuPDF (fitz)
- pdfplumber
- Pydantic
- Groq API
- Uvicorn

---

# Project Structure

```
tri9t-ai-assignment/
│
├── app/
│   ├── api/
│   ├── db/
│   ├── llm/
│   ├── models/
│   ├── parser/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── uploads/
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/<dhanush123445>/tri9t-ai-assignment.git
```

```bash
cd tri9t-ai-assignment
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=sqlite:///./tri9t.db

GROQ_API_KEY=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
```


---

# Run the Application

```bash
uvicorn app.main:app --reload
```

The server starts at

```
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## Upload Document

```
POST /documents/upload
```

Uploads a PDF document and creates a new document version.

---

## Get Tree

```
GET /tree/{version_id}
```

Returns the hierarchical tree of parsed document nodes.

---

## Get Tree Node

```
GET /tree/node/{node_id}
```

Returns information for a specific node.

---

## Search

```
GET /search
```

Parameters

```
q
version_id
```

Searches headings and body content.

Example

```
GET /search?q=battery&version_id=5
```

---

## Create Selection

```
POST /selection
```

Stores selected nodes.

Example

```json
{
    "name":"Battery Tests",
    "version_id":5,
    "node_ids":[4,8]
}
```

---

## Get Selection

```
GET /selection/{selection_id}
```

Returns previously saved selection.

---

## Generate Test Cases

```
POST /generate
```

Example

```
POST /generate?document=Battery Life: Four AA batteries provide approximately 300 measurements.
```

Returns structured JSON containing generated test cases.

---

## Compare Versions

```
POST /compare
```

Example

```json
{
    "old_version_id":5,
    "new_version_id":6
}
```

Returns

- Added nodes
- Removed nodes
- Modified nodes
- Unchanged nodes

---

# Testing

Open Swagger

```
http://127.0.0.1:8000/docs
```

Test APIs in the following order

1. Upload Document
2. Get Tree
3. Search
4. Create Selection
5. Get Selection
6. Generate Test Cases
7. Compare Versions

---

# Version Re-ingestion Flow (v1 → v2)

1. Upload a PDF document.

```
POST /documents/upload
```

Version 1 is created.

2. Modify the PDF document.

3. Upload the modified PDF again.

A new version is created automatically.

4. Compare both versions.

```
POST /compare
```

Example

```json
{
    "old_version_id":1,
    "new_version_id":2
}
```

The API identifies

- Added sections
- Removed sections
- Modified sections
- Unchanged sections

---

# Design Decisions

- PyMuPDF is used for text extraction.
- OCR is used as a fallback for scanned PDFs.
- A stack-based hierarchy algorithm builds the document tree.
- SHA-256 hashes are used to compare document nodes across versions.
- Groq Llama 3.3 generates structured JSON test cases.

---

# Known Limitations

- OCR accuracy depends on scan quality.
- Heading detection assumes numbered headings.
- Tables spanning multiple pages may require additional processing.
- Hash-based comparison cannot detect semantic changes with identical text.

---

# Future Improvements

- PostgreSQL support
- Docker deployment
- Background task processing
- Semantic search using embeddings
- Vector database integration
- Improved OCR pipeline
- LLM retry strategy

---

# Author

**Dhanush Gaja**

TRI9T AI Assignment
