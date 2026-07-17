# TRI9T AI Assignment – Approach Document

## Author

Dhanush Gaja

---

# 1. Objective

The objective of this project is to build a document intelligence system capable of:

- Parsing PDF documents
- Creating a hierarchical document tree
- Supporting document versioning
- Searching document contents
- Saving node selections
- Generating AI-powered software test cases
- Comparing different versions of a document

---

# 2. Overall Architecture

The system is divided into the following modules:

1. Document Upload
2. PDF Parser
3. Tree Builder
4. Search Engine
5. Selection Manager
6. LLM Generator
7. Version Comparison

Each module is implemented independently using FastAPI services.

---

# 3. Document Parsing

The uploaded PDF is processed using PyMuPDF.

For each page:

- Extract text
- Detect headings
- Detect numbered sections
- Extract paragraphs
- Extract tables
- Build document nodes

Each node stores:

- Logical ID
- Heading
- Level
- Body
- Content hash

---

# 4. Tree Parsing Strategy

The parser builds a hierarchical tree using heading levels.

Example

```
1

1.1

1.2

2

2.1

2.1.1
```

A stack is maintained while parsing.

If the current heading has:

- Higher level → child node
- Same level → sibling
- Lower level → move back to parent

This creates the complete hierarchy automatically.

---

# 5. Handling Parsing Irregularities

Several document irregularities are handled.

## Missing Heading Numbers

If a heading number is missing, the parser uses the previous heading level to infer the hierarchy.

---

## Multi-line Headings

Multi-line headings are merged into a single heading before creating a node.

---

## Paragraph Continuation

Paragraphs split across pages are combined into a single node body.

---

## Tables

Tables are extracted separately and stored as node content.

---

## OCR Fallback

If no selectable text is found inside a page, OCR is used as a fallback to extract text.

---

# 6. Data Model

The database contains the following entities.

## Document

Stores uploaded document information.

Fields

- id
- filename

---

## Version

Stores each uploaded version.

Fields

- id
- document_id
- version_number

---

## Node

Stores parsed document sections.

Fields

- logical_id
- heading
- body
- level
- content_hash

---

## Selection

Stores user-selected nodes.

---

# 7. Version Matching Strategy

Each node generates a SHA-256 hash using

```
Heading + Body
```

During comparison:

If hash exists in both versions

→ Unchanged

If hash exists only in new version

→ Added

If hash exists only in old version

→ Removed

If logical ID matches but hash differs

→ Modified

This approach provides fast document comparison.

---

# 8. Search Strategy

Search works on

- Heading
- Body

using SQL LIKE queries.

Example

```
battery
```

returns every matching node.

---

# 9. Selection Strategy

Users can save important nodes.

A selection contains:

- name
- version_id
- list of node IDs

Selections can later be retrieved for generating AI test cases.

---

# 10. LLM Prompt Design

Groq Llama 3.3 is used for test generation.

The prompt instructs the model to return ONLY valid JSON.

The expected JSON format is

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

The prompt also specifies

- No markdown
- No explanations
- No extra text

This improves JSON consistency.

---

# 11. Structured Output Strategy

The application validates the LLM response.

Steps:

1. Generate response
2. Parse JSON
3. Return JSON to client

If invalid JSON is received, an error is returned.

---

# 12. Retry Strategy

If the LLM produces invalid JSON:

- Parse attempt fails
- Error is detected
- Request can be retried

A future improvement is automatic retry with a stricter prompt.

---

# 13. API Workflow

Upload

↓

Parse PDF

↓

Create Tree

↓

Search Nodes

↓

Save Selection

↓

Generate Test Cases

↓

Compare Versions

---

# 14. Known Limitations

Current limitations include:

- OCR accuracy depends on scan quality.
- Tables with complex layouts may not parse correctly.
- Heading detection assumes numbered headings.
- Hash comparison cannot detect semantic similarity if text changes significantly.

---

# 15. Future Improvements

Possible enhancements:

- PostgreSQL support
- Docker deployment
- Background processing
- Semantic search using embeddings
- Vector database integration
- Automatic LLM retry
- Better OCR preprocessing

---

# 16. Conclusion

The project successfully implements a document intelligence pipeline capable of parsing technical PDF documents, generating structured document trees, comparing versions, performing searches, storing selections, and generating AI-powered software test cases using Groq Llama 3.3.
