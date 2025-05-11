import os
import logging
import json
from io import BytesIO
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from pydantic import BaseModel
from neo4j import GraphDatabase, basic_auth


# Load and verify .env file
env_path = find_dotenv()
logger.info(f"Loading environment variables from: {env_path or 'No .env file found'}")
load_dotenv(env_path)

# Log key Neo4j settings (masking password)
logger.info(f"NEO4J_URI = {os.getenv('NEO4J_URI')}")
logger.info(f"NEO4J_USER = {os.getenv('NEO4J_USER')}")

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "NTvoXpq30oKwoTzo26XMHAMKXel3HSgbWHHsTXMQPvs")  # Replace with your actual password

# Create FastAPI app
app = FastAPI(
    title="Bank Statement Graph API",
    description="API for uploading and processing bank statements into a graph model",
    version="1.0.0"
)


class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    category: Optional[str] = None


class UploadResponse(BaseModel):
    status: str
    transactions_processed: int
    filename: str
    summary: Dict[str, Any]


def get_neo4j_driver():
    """
    Creates and returns a Neo4j driver.
    """
    try:
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)
        )
        driver.verify_connectivity()
        logger.info("✅ Connected successfully to Neo4j")
        return driver
    except Exception as e:
        logger.error(f"❌ Could not connect to Neo4j: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to Neo4j database: {str(e)}"
        )


@app.get("/")
async def root():
    """Health check endpoint"""
    try:
        with get_neo4j_driver() as driver:
            return {"message": "API is up", "database": "Connected to Neo4j"}
    except HTTPException:
        return {"message": "API is up", "database": "Neo4j connection failed"}


@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    """
    Upload a bank statement file (CSV, Excel, or PDF) and process into a graph model.
    """
    logger.info(f"Upload endpoint hit, filename: {file.filename}")

    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Read file bytes
    try:
        data = await file.read()
        if len(data) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Save raw upload for inspection
    save_dir = os.path.join(os.getcwd(), "bank_statements", "raw")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file.filename)
    try:
        with open(save_path, "wb") as f:
            f.write(data)
        logger.info(f"Saved uploaded file to: {save_path}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        # Continue processing even if we couldn't save the file locally

    # Parse based on file extension
    try:
        filename = file.filename.lower()
        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(data))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(BytesIO(data))
        elif filename.endswith(".pdf"):
            df = parse_pdf_to_df(data)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")
    except Exception as e:
        logger.error(f"Error parsing file: {e}")
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

    # Debug: log parsed DataFrame sample and size
    logger.info(f"Parsed DataFrame rows: {len(df)}")
    try:
        logger.info(f"Parsed data sample: {df.head().to_dict(orient='records')}")
    except Exception as e:
        logger.warning(f"Could not log DataFrame sample: {e}")

    # Validate DataFrame
    if df.empty:
        raise HTTPException(status_code=400, detail="No transactions found in file")

    # Clean column names - trim whitespace and lowercase
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Ensure required columns exist
    required_columns = ['date', 'description', 'amount']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        # Try to guess columns if they're missing
        if 'date' not in df.columns and any('date' in col.lower() for col in df.columns):
            date_col = next(col for col in df.columns if 'date' in col.lower())
            df['date'] = df[date_col]
            missing_columns.remove('date')
            
        if 'description' not in df.columns:
            desc_candidates = [col for col in df.columns if any(term in col.lower() for term in ['desc', 'narr', 'part', 'ref', 'note'])]
            if desc_candidates:
                df['description'] = df[desc_candidates[0]]
                missing_columns.remove('description')
                
        if 'amount' not in df.columns:
            amount_candidates = [col for col in df.columns if any(term in col.lower() for term in ['amount', 'sum', 'value', 'debit', 'credit'])]
            if amount_candidates:
                df['amount'] = df[amount_candidates[0]]
                missing_columns.remove('amount')
    
    if missing_columns:
        raise HTTPException(
            status_code=400, 
            detail=f"Missing required columns: {', '.join(missing_columns)}. Available columns: {', '.join(df.columns)}"
        )

    # Convert amount to float if it's not already
    try:
        df['amount'] = pd.to_numeric(df['amount'].astype(str).str.replace(',', '').str.replace('$', ''), errors='coerce')
        # Drop rows with NaN amounts
        df = df.dropna(subset=['amount'])
    except Exception as e:
        logger.error(f"Error converting amount to numeric: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing amount column: {str(e)}")

    # Add categories to transactions
    categorized_df = categorize_transactions(df)

    # Debug: log categorized DataFrame sample and size
    logger.info(f"Categorized DataFrame rows: {len(categorized_df)}")
    try:
        logger.info(f"Categorized data sample: {categorized_df.head().to_dict(orient='records')}")
    except Exception as e:
        logger.warning(f"Could not log categorized DataFrame sample: {e}")
    
    # Process transactions and store in Neo4j
    try:
        # Generate a unique batch ID for this upload
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        batch_id = f"{os.path.splitext(file.filename)[0]}_{timestamp}"
        
        # Create a list of transaction dictionaries
        transactions = categorized_df[['date', 'description', 'amount', 'category']].to_dict(orient="records")
        
        # Add batch_id to each transaction
        for tx in transactions:
            tx['batch_id'] = batch_id
        
        # Create a summary of the transactions
        summary = {
            "total_transactions": len(transactions),
            "total_amount": round(float(categorized_df['amount'].sum()), 2),
            "average_amount": round(float(categorized_df['amount'].mean()), 2),
            "min_amount": round(float(categorized_df['amount'].min()), 2),
            "max_amount": round(float(categorized_df['amount'].max()), 2),
            "positive_transactions": int((categorized_df['amount'] > 0).sum()),
            "negative_transactions": int((categorized_df['amount'] < 0).sum()),
            "categories": summarize_categories(categorized_df)
        }
        
        # Store in Neo4j
        with get_neo4j_driver() as driver:
            result = create_graph_model(driver, transactions, batch_id, file.filename)
            logger.info(f"Created graph model with {result['nodes_created']} nodes and {result['relationships_created']} relationships")
        
        # Also save as JSON for backup
        processed_dir = os.path.join(os.getcwd(), "bank_statements", "processed")
        os.makedirs(processed_dir, exist_ok=True)
        processed_filename = f"{batch_id}.json"
        
        data_to_save = {
            "metadata": {
                "batch_id": batch_id,
                "original_filename": file.filename,
                "processed_date": datetime.now().isoformat(),
                "summary": summary
            },
            "transactions": transactions
        }
        
        save_path = os.path.join(processed_dir, processed_filename)
        with open(save_path, "w") as f:
            json.dump(data_to_save, f, indent=2)
            
        logger.info(f"Successfully processed and saved {len(transactions)} transactions to {save_path}")
        
        return UploadResponse(
            status="success",
            transactions_processed=len(transactions),
            filename=file.filename,
            summary=summary
        )
        
    except HTTPException as e:
        # Re-raise existing HTTPExceptions
        raise
    except Exception as e:
        logger.error(f"Error processing transactions: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing transactions: {str(e)}")


def parse_pdf_to_df(data: bytes) -> pd.DataFrame:
    """
    Extracts text from a PDF using PyPDF2 and converts it to a pandas DataFrame.
    Assumes each transaction is on its own line and columns are separated by whitespace.
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        logger.error("PyPDF2 is not installed – PDF parsing disabled.")
        raise HTTPException(
            status_code=500,
            detail="PDF parsing dependency missing. Please install PyPDF2."
        )

    reader = PdfReader(BytesIO(data))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    lines = [line for line in text.split("\n") if line.strip()]
    records = []
    
    # Skip header lines - usually first line is header
    if lines and len(lines) > 1:
        lines = lines[1:]
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:  # Need at least date, description, amount
            try:
                # Attempt to parse date (first column)
                date = parts[0]
                
                # Amount is usually the last column
                amount_str = parts[-1].replace(",", "").replace("$", "")
                try:
                    amount = float(amount_str)
                except ValueError:
                    # Skip lines where amount can't be converted to float
                    continue
                
                # Description is everything in between
                description = " ".join(parts[1:-1])
                records.append({
                    "date": date, 
                    "description": description, 
                    "amount": amount
                })
            except Exception as e:
                # Skip problematic lines but continue processing
                logger.warning(f"Skipped line due to error: {e}. Line: {line}")
                continue

    if not records:
        logger.warning("No valid transactions found in PDF")
        return pd.DataFrame(columns=["date", "description", "amount"])
        
    return pd.DataFrame(records)


def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize transactions based on keywords in the description.
    Returns the dataframe with an added 'category' column.
    """
    # Define categories and keywords
    categories = {
        "dining": ["restaurant", "cafe", "coffee", "pizza", "burger", "food", "dining", "eat"],
        "shopping": ["amazon", "walmart", "target", "shop", "store", "market", "retail"],
        "utilities": ["electric", "water", "gas", "internet", "phone", "utility", "bill"],
        "transportation": ["uber", "lyft", "taxi", "transit", "transport", "fuel", "gas station"],
        "entertainment": ["movie", "theatre", "netflix", "spotify", "subscription", "game"],
        "housing": ["rent", "mortgage", "property", "home", "apartment", "housing"],
        "healthcare": ["doctor", "hospital", "clinic", "pharmacy", "medical", "health", "dental"],
        "income": ["salary", "deposit", "paycheck", "income", "payment received"]
    }
    
    # Create a copy of the dataframe for categorization
    categorized_df = df.copy()
    categorized_df['category'] = 'other'
    
    # Categorize transactions
    for category, keywords in categories.items():
        mask = categorized_df['description'].str.lower().str.contains('|'.join(keywords), na=False)
        categorized_df.loc[mask, 'category'] = category
        
    return categorized_df


def summarize_categories(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Creates a summary of transactions by category.
    """
    category_summary = {}
    for category in df['category'].unique():
        category_df = df[df['category'] == category]
        category_summary[category] = {
            "count": len(category_df),
            "total_amount": round(float(category_df['amount'].sum()), 2),
            "average_amount": round(float(category_df['amount'].mean()), 2)
        }
    
    return category_summary


def create_graph_model(driver: GraphDatabase.driver, transactions: List[Dict], batch_id: str, filename: str) -> Dict:
    """
    Creates a graph model from the transactions data.
    
    The graph model consists of:
    - Transaction nodes with properties (date, amount, description)
    - Category nodes
    - Merchant nodes (extracted from descriptions)
    - BatchUpload nodes to group transactions
    - Relationships between these nodes
    
    Returns a dictionary with counts of created nodes and relationships.
    """
    with driver.session() as session:
        # First create the BatchUpload node
        session.run("""
            CREATE (b:BatchUpload {
                batch_id: $batch_id,
                filename: $filename,
                upload_date: datetime(),
                transaction_count: $count
            })
        """, batch_id=batch_id, filename=filename, count=len(transactions))
        
        # Then create Transaction nodes and link to BatchUpload
        # Also create Category nodes and link to Transactions
        result = session.run("""
            MATCH (b:BatchUpload {batch_id: $batch_id})
            
            UNWIND $transactions AS tx
            
            // Create Transaction node
            CREATE (t:Transaction {
                transaction_id: apoc.create.uuid(),
                date: tx.date,
                description: tx.description,
                amount: tx.amount,
                batch_id: tx.batch_id
            })
            
            // Link Transaction to BatchUpload
            CREATE (t)-[:PART_OF]->(b)
            
            // Create or match Category node and link to Transaction
            MERGE (c:Category {name: tx.category})
            CREATE (t)-[:CATEGORIZED_AS]->(c)
            
            // Extract merchant name from description (simplified approach)
            WITH t, b, c, tx, 
                 CASE 
                    WHEN size(split(tx.description, ' ')) > 1 
                    THEN split(tx.description, ' ')[0] + ' ' + split(tx.description, ' ')[1]
                    ELSE tx.description 
                 END AS merchant_name
            
            // Create or match Merchant node and link to Transaction
            MERGE (m:Merchant {name: merchant_name})
            CREATE (t)-[:FROM_MERCHANT]->(m)
            
            // Return counts for reporting
            RETURN count(t) as transactions_created
        """, batch_id=batch_id, transactions=transactions)
        
        # Collect statistics
        for record in result:
            transactions_created = record["transactions_created"]
        
        # Create additional relationships based on transaction patterns
        session.run("""
            // Create relationships between merchants in the same category
            MATCH (m1:Merchant)<-[:FROM_MERCHANT]-(t1:Transaction)-[:CATEGORIZED_AS]->(c:Category),
                  (m2:Merchant)<-[:FROM_MERCHANT]-(t2:Transaction)-[:CATEGORIZED_AS]->(c)
            WHERE m1 <> m2 AND t1.batch_id = $batch_id AND t2.batch_id = $batch_id
            MERGE (m1)-[r:SAME_CATEGORY]->(m2)
            SET r.category = c.name
            
            // Create time-based sequence relationships between transactions
            MATCH (t1:Transaction), (t2:Transaction)
            WHERE t1.batch_id = $batch_id AND t2.batch_id = $batch_id
                  AND t1.date = t2.date AND id(t1) < id(t2)
            MERGE (t1)-[:SAME_DAY]->(t2)
        """, batch_id=batch_id)
        
        # Query to get counts of created nodes and relationships
        result = session.run("""
            MATCH (n)
            WHERE n.batch_id = $batch_id OR 
                  EXISTS((n)<-[:CATEGORIZED_AS|FROM_MERCHANT]-(:Transaction {batch_id: $batch_id}))
            WITH count(n) as nodes_created
            
            MATCH ()-[r]->()
            WHERE r.batch_id = $batch_id OR
                  EXISTS((:Transaction {batch_id: $batch_id})-[r]->()) OR
                  EXISTS(()-[r]->(:Transaction {batch_id: $batch_id}))
            RETURN nodes_created, count(r) as relationships_created
        """, batch_id=batch_id)
        
        stats = result.single()
        return {
            "nodes_created": stats["nodes_created"],
            "relationships_created": stats["relationships_created"],
            "transactions_created": transactions_created
        }


@app.get("/graph/summary")
async def get_graph_summary():
    """
    Get a summary of what's in the graph database.
    """
    try:
        with get_neo4j_driver() as driver:
            with driver.session() as session:
                # Get counts of different types of nodes
                result = session.run("""
                    MATCH (n)
                    WITH labels(n)[0] as node_type, count(n) as count
                    RETURN node_type, count
                    ORDER BY count DESC
                """)
                node_counts = {record["node_type"]: record["count"] for record in result}
                # Get counts of different types of relationships
                result = session.run("""
                    MATCH ()-[r]->()
                    WITH type(r) as rel_type, count(r) as count
                    RETURN rel_type, count
                    ORDER BY count DESC
                """)
                relationship_counts = {record["rel_type"]: record["count"] for record in result}
                # Get batch upload information
                result = session.run("""
                    MATCH (b:BatchUpload)
                    RETURN b.batch_id as batch_id, 
                           b.filename as filename, 
                           b.upload_date as upload_date,
                           b.transaction_count as transaction_count
                    ORDER BY b.upload_date DESC
                """)
                batches = []
                for record in result:
                    batches.append({
                        "batch_id": record["batch_id"],
                        "filename": record["filename"],
                        "upload_date": record["upload_date"],
                        "transaction_count": record["transaction_count"]
                    })
                return {
                    "node_counts": node_counts,
                    "relationship_counts": relationship_counts,
                    "batches": batches
                }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting graph summary: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error getting graph summary.")


@app.get("/graph/query")
async def run_graph_query(query: str):
    """
    Run a custom Cypher query against the graph database.
    WARNING: This endpoint should be properly secured in production!
    """
    try:
        with get_neo4j_driver() as driver:
            with driver.session() as session:
                result = session.run(query)
                records = [record.data() for record in result]
                return {"results": records}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error running graph query: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error running graph query.")


@app.get("/graph/categories")
async def get_category_analysis():
    """
    Get an analysis of transactions by category.
    """
    try:
        with get_neo4j_driver() as driver:
            with driver.session() as session:
                result = session.run("""
                    MATCH (t:Transaction)-[:CATEGORIZED_AS]->(c:Category)
                    WITH c.name as category, count(t) as transaction_count, sum(t.amount) as total_amount,
                         avg(t.amount) as avg_amount
                    RETURN category, transaction_count, total_amount, avg_amount
                    ORDER BY transaction_count DESC
                """)
                categories = []
                for record in result:
                    categories.append({
                        "category": record["category"],
                        "transaction_count": record["transaction_count"],
                        "total_amount": round(record["total_amount"], 2),
                        "average_amount": round(record["avg_amount"], 2)
                    })
                return {"categories": categories}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting category analysis: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error getting category analysis.")


@app.get("/graph/merchants")
async def get_merchant_analysis():
    """
    Get an analysis of top merchants by transaction count.
    """
    try:
        with get_neo4j_driver() as driver:
            with driver.session() as session:
                result = session.run("""
                    MATCH (t:Transaction)-[:FROM_MERCHANT]->(m:Merchant)
                    WITH m.name as merchant, count(t) as transaction_count, sum(t.amount) as total_amount,
                         collect(t.category)[0] as common_category
                    RETURN merchant, transaction_count, total_amount, common_category
                    ORDER BY transaction_count DESC
                    LIMIT 20
                """)
                merchants = []
                for record in result:
                    merchants.append({
                        "merchant": record["merchant"],
                        "transaction_count": record["transaction_count"],
                        "total_amount": round(record["total_amount"], 2),
                        "common_category": record["common_category"]
                    })
                return {"merchants": merchants}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting merchant analysis: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error getting merchant analysis.")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)