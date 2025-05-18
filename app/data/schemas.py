from typing import Any, Dict, Optional
from pydantic import BaseModel

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