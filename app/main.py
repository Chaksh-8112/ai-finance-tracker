from fastapi import FastAPI, File, UploadFile, HTTPException
from neo4j import GraphDatabase, exceptions
import pandas as pd
from io import BytesIO
import logging
import os
from dotenv import load_dotenv
load_dotenv()

# Neo4j driver import and initialization
try:
    
    # Initialize Neo4j driver
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    try:
        driver.verify_connectivity()
        logging.info("✅ Connected successfully to Neo4j!")
    except exceptions.ServiceUnavailable as e:
        logging.error(f"❌ Could not connect to Neo4j: {e}")
except ImportError:
    logging.error("Neo4j driver not installed – database functionality disabled.")
    driver = None

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
async def root():
    logging.info("Root endpoint hit")
    return {"message": "API is up"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    logging.info(f"Upload endpoint hit, filename: {file.filename}")
    data = await file.read()
    # Ensure the bank_statements folder exists
    save_dir = os.path.join(os.getcwd(), "bank_statements")
    os.makedirs(save_dir, exist_ok=True)
    # Save the raw upload for inspection
    save_path = os.path.join(save_dir, file.filename)
    with open(save_path, "wb") as f:
        f.write(data)
    logging.info(f"Saved uploaded file to: {save_path}")
    filename = file.filename.lower()
    if filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(data))
    elif filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(BytesIO(data))
    elif filename.endswith(".pdf"):
        df = parse_pdf_to_df(data)
    else:
        raise ValueError(f"Unsupported file type: {file.filename}")

    # Send parsed DataFrame into Neo4j
    send_df_to_neo4j(df)

    # your parsing + ingest logic
    return {"status": "ok"}

def parse_pdf_to_df(data: bytes) -> pd.DataFrame:
    """
    Extracts text from a PDF using PyPDF2 and converts it to a pandas DataFrame.
    Assumes each transaction is on its own line and columns are separated by whitespace.
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        logging.error("PyPDF2 is not installed – PDF parsing disabled.")
        raise HTTPException(status_code=500, detail="PDF parsing dependency missing. Please install PyPDF2.")
    # Read PDF bytes via PyPDF2
    reader = PdfReader(BytesIO(data))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    # Split into non-empty lines
    lines = [line for line in text.split("\n") if line.strip()]
    # Parse each line into date, description, amount
    records = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            date = parts[0]
            amount_str = parts[-1].replace(",", "")
            try:
                amount = float(amount_str)
            except ValueError:
                continue
            description = " ".join(parts[1:-1])
            records.append({"date": date, "description": description, "amount": amount})
    return pd.DataFrame(records)

def send_df_to_neo4j(df: pd.DataFrame):
    """
    Sends rows in df to Neo4j as Transaction nodes.
    """
    if driver is None:
        logging.error("Attempted to write to Neo4j but driver is unavailable.")
        raise HTTPException(status_code=500, detail="Neo4j driver not installed. Please install `neo4j`.")
    records = df.to_dict(orient="records")
    with driver.session(database="neo4j") as session:
        session.run(
            """
            UNWIND $records AS rec
            CREATE (:Transaction {
                date: rec.date,
                description: rec.description,
                amount: rec.amount
            })
            """,
            records=records
        )