# Neo4j Overview

## What is Neo4j?

Neo4j is a highly performant, native graph database that stores data as nodes, relationships, and properties. It is designed to handle connected data and complex queries efficiently, making it ideal for use cases involving relationships and networks.

## Core Concepts

- **Nodes**: Represent entities or objects in the graph, such as users, products, or transactions.
- **Relationships**: Directed connections between nodes that define how entities are related.
- **Properties**: Key-value pairs attached to nodes or relationships to store relevant information.
- **Cypher**: Neo4j’s declarative query language used to create, read, update, and delete data in the graph.

## Use Case: Modeling Transactions

In this project, transactions are modeled as nodes connected by relationships to capture spending patterns and categories. This graph structure allows for rich querying and analysis of financial data, such as identifying recurring expenses or grouping transactions by category and date.

## Connection & Driver

To interact with Neo4j using Python, the official Neo4j Python driver is used. Configuration typically involves specifying the URI, username, and password, then establishing a session for executing Cypher queries.

```python
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

def close_driver():
    driver.close()
```

## Bulk Data Loading: UNWIND Pattern

The `UNWIND` clause in Cypher is used to efficiently load and process lists of data in bulk. It is especially useful for importing multiple transactions or nodes in a single query, improving performance and reducing the number of calls to the database.

```cypher
UNWIND $transactions AS transaction
MERGE (t:Transaction {id: transaction.id})
SET t += transaction
```

## Enrichment Patterns

To enrich the graph, relationships such as `SAME_CATEGORY` and `SAME_DAY` are created between transactions. These patterns enable advanced analysis by connecting transactions that share common attributes, facilitating queries like grouping expenses by category or analyzing daily spending behavior.

## Further Reading

- [Neo4j Documentation](https://neo4j.com/docs/)
- [APOC Library (Awesome Procedures On Cypher)](https://neo4j.com/labs/apoc/) - A powerful plugin that extends Cypher with many useful procedures and functions.
# ai-finance-tracker

A FastAPI application that parses bank statements (CSV, Excel, PDF), categorizes transactions, and stores them in a Neo4j graph for analysis.

## Prerequisites

- Python 3.9+
- Poetry
- Neo4j Aura Free or local Neo4j instance
- Git

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/ai-finance-tracker.git
   cd ai-finance-tracker
   ```

2. **Install dependencies**  
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**  
   ```bash
   poetry shell
   ```

## Configuration

1. **Environment variables**  
   Create a file named `.env` in the project root with the following variables:

   ```dotenv
   # Neo4j connection (Aura Free or local)
   NEO4J_URI=bolt+ssc://<your-cluster-id>.databases.neo4j.io:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=<your-password>

   # (Optional) Directory for uploaded bank statements
   BANK_STATEMENT_DIR=bank_statements/raw
   ```

2. **Ensure `.env` is ignored**  
   Add `.env` to `.gitignore` if not already present.

## Running the Server

Start the FastAPI server with hot reload:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### OpenAPI Docs

- Browse interactive API docs at:  
  ```
  http://127.0.0.1:8000/docs
  ```

### Upload Statement

- **Endpoint:** `POST /upload`  
- **Description:** Upload a bank statement file. Supported formats: CSV, XLS, XLSX, PDF.  
- **Usage (curl example):**

  ```bash
  curl -X POST "http://127.0.0.1:8000/upload" \
       -F "file=@/path/to/statement.pdf"
  ```

- **Response:**  
  ```json
  {
    "status": "ok"
  }
  ```

### Graph Endpoints

Once data is loaded in Neo4j, query and analyze the graph:

- **GET /graph/summary**  
  Returns counts of node types, relationship types, and recent batch uploads.

- **GET /graph/query?query=<cypher>**  
  Run a custom Cypher query. WARNING: secure in production.

- **GET /graph/categories**  
  Returns analysis of transactions by category (counts, totals, averages).

- **GET /graph/merchants**  
  Returns top merchants by transaction count.

## Neo4j Integration

Data is loaded into Neo4j with a batch-based model:

1. **BatchUpload node** for each file, tracking filename, upload time, and transaction count.
2. **Transaction nodes** with properties: date, description, amount, batch_id.
3. **Category and Merchant nodes** linked via `CATEGORIZED_AS` and `FROM_MERCHANT`.
4. **Relationship enrichment** with `SAME_CATEGORY` and `SAME_DAY`.

See `app/main.py` and `create_graph_model` for full Cypher patterns.

## License

MIT License.