# TRI9T AI Assignment – Approach Document

**Author:** Dhanush Gaja

---

# 1. Introduction

The objective of this project is to build a document intelligence system capable of:

- Uploading PDF documents
- Parsing technical documents into a hierarchical tree
- Supporting document versioning
- Searching document contents
- Saving user selections
- Generating AI-powered software test cases
- Comparing different document versions

The application is implemented using **FastAPI**, **SQLAlchemy**, **SQLite**, **PyMuPDF**, **pdfplumber**, and **Groq Llama 3.3**.

---

# 2. System Architecture

The application is divided into the following modules:

1. Document Upload
2. PDF Parser
3. Tree Reconstruction
4. Search API
5. Selection API
6. LLM Test Case Generator
7. Version Comparison

Each module is independent and exposed through REST APIs.

---

# 3. Data Model

The database is implemented using SQLAlchemy ORM.

## Document

Stores uploaded documents.

Fields:

- id
- filename
- created_at

One document can contain multiple versions.

---

## Version

Stores every uploaded version of a document.

Fields:

- id
- document_id
- version_number
- uploaded_at

Each upload creates a new version.

---

## Node

Each heading extracted from the PDF becomes a node.

Fields:

- id
- version_id
- logical_id
- heading
- body
- level
- content_hash

Nodes together form the complete document tree.

---

## Selection

Stores user-created node selections.

Fields:

- id
- name
- version_id

---

## SelectionNode

Stores the mapping between selections and nodes.

---

# 4. OCR / Document Parsing Approach

The parser processes uploaded PDFs using **PyMuPDF (fitz)**.

For every page:

- Extract text blocks
- Detect headings
- Build hierarchy
- Store body text
- Extract tables

### Why PyMuPDF?

PyMuPDF was selected because:

- Fast text extraction
- Preserves reading order
- Easy page-level access
- Supports large PDFs efficiently

### Why pdfplumber?

Technical manuals contain tables.

pdfplumber provides much better table extraction than PyMuPDF.

Tables are extracted separately and attached to their corresponding nodes.

### OCR Fallback

Some PDFs contain scanned pages with no selectable text.

If PyMuPDF returns no text blocks, the parser automatically falls back to OCR extraction.

This improves support for scanned documents.

---

# 5. Hierarchy Reconstruction Strategy

The parser reconstructs the document hierarchy using heading numbering.

Example:

```
1

1.1

1.2

2

2.1

2.1.1
```

A stack is maintained while parsing.

Algorithm:

- Higher level → Child node
- Same level → Sibling node
- Lower level → Pop stack until correct parent

This guarantees a correct hierarchical structure.

---

# 6. Structural Inconsistencies and Edge Cases

During development, several irregularities were observed.

## Empty Text Blocks

Some pages contained empty blocks.

Solution:

Ignore blank blocks.

---

## Multi-line Headings

Some headings were split across multiple lines.

Solution:

Merge heading text before creating nodes.

---

## Paragraph Continuation

Paragraphs often continue onto the next page.

Solution:

Continue appending text until a new heading appears.

---

## Nested Sections

Some documents contained deeply nested sections.

Example:

```
2

2.1

2.1.1

2.1.1.1
```

Solution:

Stack-based hierarchy reconstruction.

---

## Tables

Tables interrupt normal text flow.

Solution:

Extract tables separately and attach them after parsing.

---

## Scanned Pages

Some pages contained only images.

Solution:

OCR fallback.

---

# 7. Initial Implementation Limitations

The initial implementation had several issues.

### process_text() Error

The process_text() function was accidentally indented inside another method.

This produced:

```
AttributeError:
PDFParser object has no attribute process_text
```

This was fixed by correcting indentation.

---

### Table Attachment

Initially tables were extracted but not attached to document nodes.

Later versions correctly attached tables based on page number.

---

### OCR

The first implementation ignored scanned documents.

OCR fallback was later introduced.

---

### LLM Output

Initially the LLM returned Markdown instead of JSON.

The prompt was redesigned to enforce strict JSON output.

---

### JSON Parsing

Some responses contained invalid JSON.

Validation was added before returning the response.

---

# 8. Failure Identification

Failures were identified using multiple techniques.

## Manual Inspection

The tree endpoint was used to inspect extracted headings.

```
GET /tree/{version_id}
```

---

## Search Validation

The search endpoint confirmed body extraction.

```
GET /search
```

---

## Version Comparison

Two document versions were uploaded.

The compare endpoint verified:

- Added nodes
- Removed nodes
- Modified nodes

---

## Visual Comparison

Extracted headings were compared against the original PDF.

---

## API Testing

Swagger UI was used to test every endpoint.

---

# 9. Improvements Made

Several improvements were introduced during development.

- Added OCR fallback.
- Improved heading detection.
- Added stack-based hierarchy reconstruction.
- Implemented SHA-256 hashing.
- Added table extraction.
- Improved JSON prompt.
- Added JSON validation.
- Improved node attachment logic.

These significantly improved extraction quality.

---

# 10. Version Matching Strategy

Each node receives a SHA-256 content hash.

Hash is generated from:

- Heading
- Body
- Level
- Hierarchical path

Comparison rules:

## Unchanged

Same hash in both versions.

---

## Added

Present only in new version.

---

## Removed

Present only in old version.

---

## Modified

Logical ID exists in both versions but hashes differ.

This approach is fast and deterministic.

---

# 11. Known Failure Modes

The current implementation has some limitations.

## OCR Accuracy

Depends on scan quality.

---

## Heading Detection

Assumes numbered headings.

Documents without numbering may require different heuristics.

---

## Complex Tables

Merged cells and multi-page tables are difficult to reconstruct.

---

## Semantic Changes

Hash comparison detects textual differences only.

It cannot identify semantic equivalence.

---

## Large Documents

Large PDFs require additional processing time.

---

# 12. LLM Prompt Design

Groq Llama 3.3 is used to generate software test cases.

The prompt explicitly instructs the model to:

- Return ONLY JSON
- No Markdown
- No explanations
- Follow a predefined schema

Expected format:

```json
{
  "test_cases": [
    {
      "id": 1,
      "title": "",
      "preconditions": "",
      "steps": [],
      "expected_result": ""
    }
  ]
}
```

Providing the schema greatly improves response consistency.

---

# 13. Structured Output Strategy

The application validates every LLM response.

Workflow:

1. Generate response
2. Parse JSON
3. Validate schema
4. Return JSON

If parsing fails:

```
Invalid JSON returned from LLM
```

is returned instead of invalid data.

---

# 14. Retry Strategy

Currently:

- Invalid JSON is detected.
- The API returns an error.

Future improvement:

Automatically retry generation with a stricter prompt until valid JSON is produced.

---

# 15. What I Would Improve With More Time

Given additional development time, I would implement:

- PostgreSQL support
- Docker deployment
- Semantic document comparison using embeddings
- Vector search with FAISS
- Better OCR preprocessing
- Automatic LLM retry mechanism
- Authentication and authorization
- Background PDF processing
- Export test cases to Excel/PDF
- Semantic heading detection using machine learning

---

# 16. API Workflow

```
Upload PDF
      │
      ▼
Parse Document
      │
      ▼
Build Tree
      │
      ▼
Search Nodes
      │
      ▼
Create Selection
      │
      ▼
Generate Test Cases
      │
      ▼
Compare Versions
```

---

# 17. Conclusion

This project successfully implements an end-to-end document intelligence system capable of parsing technical PDF documents, reconstructing document hierarchy, supporting document versioning, searching document contents, generating AI-assisted software test cases, and comparing document versions.

The modular architecture makes the system easy to extend and maintain while providing a strong foundation for future improvements such as semantic search, vector databases, and intelligent version comparison.
