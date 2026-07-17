# TRI9T AI Assignment – Approach Document
 
**Author:** Dhanush Gaja
 
---
 
# 1. Introduction
 
The objective of this project is to build a backend system capable of parsing technical PDF documents into a hierarchical tree structure, supporting document versioning, searching document contents, generating AI-powered software test cases, and comparing different versions of a document.
 
The application is implemented using **FastAPI**, **SQLAlchemy**, **SQLite**, **PyMuPDF**, **pdfplumber**, and **Groq Llama 3.3**.
 
---
 
# 2. System Architecture
 
The overall workflow of the system is shown below.
 
```
                    Upload PDF
                        |
                        v
                  PDF Parser
                        |
                        v
          Hierarchy Reconstruction
                        |
                        v
                   SQLite Database
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
     Search API    Selection API   Compare API
                                        |
                                        v
                                Version Matching
 
                        |
                        v
                  Generate API
                        |
                        v
                 Groq Llama 3.3
                        |
                        v
               Software Test Cases
```
 
---
 
# 3. Data Model
 
The application stores parsed information using SQLAlchemy models.
 
## Document
 
Represents an uploaded document.
 
Fields:
 
- id
- filename
- created_at
A document can have multiple versions.
 
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
 
Every heading extracted from the PDF becomes a node.
 
Fields:
 
- id
- version_id
- logical_id
- heading
- body
- level
- content_hash
Nodes together form the hierarchical tree.
 
---
 
## Selection
 
Stores user-created selections.
 
Fields:
 
- id
- version_id
- name
---
 
## SelectionNode
 
Maps selected nodes to a selection.
 
---
 
# 4. OCR / Document Parsing Approach
 
The parser uses **PyMuPDF (fitz)** to extract text from PDF pages.
 
For each page the parser:
 
- extracts text blocks
- identifies headings
- collects paragraph text
- extracts tables
- creates tree nodes
## Why PyMuPDF?
 
PyMuPDF was selected because it:
 
- provides fast text extraction
- preserves reading order
- supports page-level processing
- performs well on large technical documents
## Why pdfplumber?
 
Technical manuals frequently contain tables.
 
pdfplumber provides better table extraction than PyMuPDF, so it is used specifically for tables.
 
## OCR Fallback
 
Some PDFs contain scanned pages without selectable text.
 
When PyMuPDF fails to extract text, OCR is used as a fallback to recover document content.
 
---
 
# 5. Hierarchy Reconstruction Strategy
 
The hierarchy is reconstructed using numbered headings.
 
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
 
Rules:
 
- Higher level → Child node
- Same level → Sibling node
- Lower level → Pop stack until correct parent
This efficiently reconstructs nested document structures.
 
---
 
# 6. Structural Inconsistencies and Edge Cases
 
During implementation several document irregularities were encountered.
 
## Empty Text Blocks
 
Some pages contained empty blocks.
 
Solution: Ignored blank text blocks.
 
---
 
## Multi-line Headings
 
Certain headings were split across multiple lines.
 
Solution: Merged lines before heading detection.
 
---
 
## Paragraph Continuation
 
Paragraphs often continued onto the next page.
 
Solution: Continue collecting text until another heading is encountered.
 
---
 
## Deeply Nested Sections
 
Example:
 
```
2
2.1
2.1.1
2.1.1.1
```
 
Solution: Stack-based hierarchy reconstruction.
 
---
 
## Tables
 
Tables interrupt normal text flow.
 
Solution: Extract tables separately using pdfplumber and attach them after parsing.
 
---
 
## Scanned PDFs
 
Scanned pages contain only images.
 
Solution: Use OCR fallback when no text is extracted.
 
---
 
# 7. Initial Implementation Limitations
 
During development several issues were encountered.
 
## process_text() Error
 
The function was incorrectly indented.
 
Result:
 
```
AttributeError:
PDFParser object has no attribute process_text
```
 
This was fixed by correcting the class indentation.
 
---
 
## Table Attachment
 
Initially tables were extracted but not attached to document nodes.
 
This was corrected by mapping tables to the appropriate page.
 
---
 
## OCR
 
The first version ignored scanned documents.
 
OCR fallback was added later.
 
---
 
## LLM Output
 
Initially the LLM returned Markdown instead of JSON.
 
The prompt was redesigned to explicitly request JSON output.
 
---
 
## Invalid JSON
 
Some responses contained malformed JSON.
 
Validation was added before returning the response.
 
---
 
# 8. Failure Identification
 
Failures were identified using several methods.
 
## Manual Inspection
 
Compared extracted headings with the original PDF.
 
---
 
## Tree API
 
Verified document hierarchy using:
 
```
GET /tree/{version_id}
```
 
---
 
## Search API
 
Verified that paragraph text was attached to the correct nodes.
 
---
 
## Compare API
 
Uploaded multiple versions and confirmed:
 
- Added nodes
- Removed nodes
- Modified nodes
---
 
## Swagger Testing
 
Every endpoint was tested through Swagger UI.
 
---
 
# 9. Improvements Made
 
Several improvements were introduced.
 
- Added OCR fallback
- Improved heading detection
- Added stack-based hierarchy reconstruction
- Implemented SHA-256 hashing
- Added table extraction
- Improved LLM prompt
- Added JSON validation
These improvements significantly increased extraction quality.
 
---
 
# 10. Version Matching Strategy
 
Each node receives a SHA-256 content hash generated from:
 
- Heading
- Body
- Level
- Logical ID
Comparison Rules
 
## Unchanged
 
Same hash.
 
---
 
## Added
 
Present only in the new version.
 
---
 
## Removed
 
Present only in the old version.
 
---
 
## Modified
 
Logical ID exists but hashes differ.
 
This strategy is deterministic and computationally efficient.
 
---
 
# 11. Known Failure Modes
 
The current implementation has some limitations.
 
## OCR Accuracy
 
Depends on scan quality.
 
---
 
## Heading Detection
 
Assumes numbered headings.
 
Documents using only formatting may not reconstruct correctly.
 
---
 
## Complex Tables
 
Merged cells and multi-page tables are difficult to reconstruct.
 
---
 
## Semantic Changes
 
Hash comparison detects textual differences but not semantic similarity.
 
---
 
## Large Documents
 
Very large PDFs increase processing time.
 
---
 
# 12. LLM Prompt Design
 
Groq Llama 3.3 is used to generate software test cases.
 
The prompt instructs the model to:
 
- Return only JSON
- No Markdown
- No explanations
- Follow a predefined schema
Example schema:
 
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
 
Providing the schema improves response consistency.
 
---
 
# 13. Structured Output Strategy
 
Every LLM response is validated.
 
Workflow:
 
1. Generate response
2. Parse JSON
3. Validate schema
4. Return JSON
If parsing fails:
 
```
Invalid JSON returned from LLM
```
 
is returned.
 
---
 
# 14. Retry Strategy
 
Current implementation:
 
- Detect invalid JSON
- Return an error
Future improvement:
 
Automatically retry the LLM call with a stricter prompt until valid JSON is generated.
 
---
 
# 15. API Workflow
 
```
Upload PDF
      |
      v
Parse Document
      |
      v
Build Tree
      |
      v
Store in Database
      |
 +----+--------------+
 v    v              v
Search Selection   Compare
            |
            v
      Generate Tests
```
 
---
 
# 16. Decision Log
 
## 16.1 What is the one part of this system most likely to silently give wrong results without throwing an error? How would you catch it?
 
The hierarchy reconstruction process is the part most likely to silently produce incorrect results. If a PDF uses inconsistent heading numbering or formatting, the parser may attach sections to the wrong parent while still producing a valid tree. Since no exception is raised, the error is difficult to detect automatically.
 
I identified these issues by manually comparing the generated tree with the original PDF and verifying the hierarchy using the `/tree/{version_id}` API. I also used the search API to ensure paragraphs were attached to the correct headings.
 
---
 
## 16.2 Where did you choose simplicity over correctness because of time, and what would break first if this went to production?
 
For version comparison, I used SHA-256 hashing of each node instead of semantic comparison. This approach is simple, deterministic, and fast to implement.
 
If deployed to production, the first limitation would be that small wording changes with the same meaning would still be reported as modified because hash comparison only detects textual differences. A semantic similarity approach using embeddings would produce more accurate results.
 
---
 
## 16.3 Name one input that you did not handle, and what your system does when it sees it.
 
The parser does not fully handle documents that use only font size or bold formatting for headings without numbering.
 
When such a document is uploaded, the text is still extracted successfully, but the hierarchy reconstruction may flatten sections or assign incorrect parent-child relationships. The application continues to run without crashing, but the resulting tree may not accurately represent the original document structure.
 
---
 
# 17. Summary
 
This implementation provides a modular document intelligence backend with PDF parsing, hierarchy reconstruction, version management, search, AI-powered test generation, and document comparison. The current solution focuses on correctness for structured technical documents while leaving opportunities for future improvements such as semantic comparison, vector search, and more advanced OCR techniques.
 
