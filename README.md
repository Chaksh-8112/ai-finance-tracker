<file name=0 path=/Users/chakshitashetty/Desktop/My_protfolio/Finance/ai-finance-tracker/README.md>

###ai-finance-tracker
## Prerequisites

- Python 3.7 or higher
- Poetry for dependency management
- A running Neo4j instance (bolt://localhost:7687) and credentials
- (Optional) Docker if you prefer to run Neo4j in a container

## Installation

```bash
# Clone the repository
git clone https://github.com/Chaksh-8112/ai-finance-tracker.git
cd ai-finance-tracker

# Install dependencies via Poetry
poetry install
```

## Activating the virtual environment

After installing dependencies, activate the Poetry-managed shell:

```bash
poetry shell
```

If `poetry shell` does not work, manually activate the virtual environment with:

```bash
source $(poetry env info --path)/bin/activate
```

## Environment Setup

1. Create a `.env` file in the project root with the following variables:
   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=yourPassword
   ```
2. Install PDF support if not already present:
   ```bash
   poetry add pdfplumber python-multipart
   ```

## Running the Server

```bash
# Start the FastAPI server with auto-reload
poetry run uvicorn app.main:app --reload
```

- The server will be available at `http://127.0.0.1:8000`.
- Interactive API docs: `http://127.0.0.1:8000/docs`

## Uploading a File

You can upload CSV, Excel, or PDF bank statements via the Swagger UI or `curl`:

- **Swagger UI**:  
  1. Open `http://127.0.0.1:8000/docs` in your browser.  
  2. Expand the **POST /upload** endpoint.  
  3. Click **Try it out**, choose your file, and execute.

- **cURL**:
  ```bash
  curl -F "file=@/path/to/statement.pdf" http://127.0.0.1:8000/upload
  ```

If `pdfplumber` is not found, ensure it is installed in your environment:
```bash
poetry add pdfplumber
```
Then restart the server.

## Verifying Uploads

Uploaded files are saved under `bank_statements/` in the project root for inspection. Check your console logs for the saved path.

<details>
<summary>High-Level Architecture (click to expand)</summary>

```mermaid
flowchart TD
  subgraph Client["Client Layer"]
    A[User] -->|Upload Statements| B[FastAPI /upload]
    A -->|Query Data| C[FastAPI /graph/*]
    A -->|View Docs| D[Swagger UI /docs]
  end

  subgraph Processing["Processing Layer"]
    B -->|PDF| E[PDF Parser\npdfplumber]
    B -->|CSV/Excel| F[Data Parser\npandas]
    E --> G[Transaction Extraction]
    F --> G
    G -->|Structured Data| H[Transaction Categorization]
    H -->|Categorized Transactions| I[Neo4j Graph Model]
  end

  subgraph Database["Database Layer"]
    I -->|Cypher Queries| J[Neo4j Driver]
    J <-->|Bolt Protocol| K[Neo4j Database]
    
    subgraph GraphModel["Graph Data Model"]
      N[Transaction]
      O[Category]
      P[Merchant]
      Q[BatchUpload]
      
      N -->|BELONGS_TO| O
      N -->|PAID_TO| P
      Q -->|CONTAINS| N
      N -->|SAME_DAY| N
      O -->|SAME_CATEGORY| O
    end
  end

  subgraph Analysis["Analysis Layer"]
    C -->|Query Request| L[Graph Analytics]
    L -->|Cypher Queries| J
    L -->|Results| M[Insights & Visualization]
    M --> A
  end

  classDef primary fill:#f9f,stroke:#333,stroke-width:2px;
  classDef secondary fill:#bbf,stroke:#333,stroke-width:1px;
  classDef tertiary fill:#ddf,stroke:#333,stroke-width:1px;
  
  class A,B,C,D primary;
  class E,F,G,H,I secondary;
  class J,K,L,M tertiary;
```
