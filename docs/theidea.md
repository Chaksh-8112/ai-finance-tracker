# Financial Graph AI

## Personal Finance Analysis with Graph Database, LLMs and Agents

Financial Graph AI is an open-source project that transforms personal bank statements into intelligent, queryable financial insights using graph database architecture and modern AI capabilities.

<div align="center">
  <svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg" width="600">
    <!-- Background -->
    <rect width="800" height="600" fill="#f8f9fa" rx="10" ry="10"/>
    
    <!-- Title -->
    <text x="400" y="40" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="#333">Financial Graph AI Architecture</text>
    
    <!-- Data Ingestion Layer -->
    <rect x="100" y="80" width="600" height="100" rx="8" ry="8" fill="#e3f2fd" stroke="#2196f3" stroke-width="2"/>
    <text x="400" y="110" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#0d47a1">Data Ingestion Layer</text>
    
    <rect x="140" y="130" width="120" height="40" rx="5" ry="5" fill="#bbdefb" stroke="#1976d2" stroke-width="1"/>
    <text x="200" y="155" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">CSV/Excel</text>
    
    <rect x="340" y="130" width="120" height="40" rx="5" ry="5" fill="#bbdefb" stroke="#1976d2" stroke-width="1"/>
    <text x="400" y="155" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">PDF Parser</text>
    
    <rect x="540" y="130" width="120" height="40" rx="5" ry="5" fill="#bbdefb" stroke="#1976d2" stroke-width="1"/>
    <text x="600" y="155" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Normalizer</text>
    
    <!-- Arrow -->
    <path d="M400,180 L400,210" stroke="#666" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
    
    <!-- Graph Database Layer -->
    <rect x="100" y="210" width="600" height="140" rx="8" ry="8" fill="#e8f5e9" stroke="#4caf50" stroke-width="2"/>
    <text x="400" y="240" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#1b5e20">Graph Database Layer</text>
    
    <!-- Graph Nodes -->
    <circle cx="200" cy="290" r="30" fill="#c8e6c9" stroke="#388e3c" stroke-width="1.5"/>
    <text x="200" y="295" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Transaction</text>
    
    <circle cx="350" cy="290" r="30" fill="#c8e6c9" stroke="#388e3c" stroke-width="1.5"/>
    <text x="350" y="295" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Merchant</text>
    
    <circle cx="500" cy="290" r="30" fill="#c8e6c9" stroke="#388e3c" stroke-width="1.5"/>
    <text x="500" y="295" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Category</text>
    
    <circle cx="650" cy="290" r="30" fill="#c8e6c9" stroke="#388e3c" stroke-width="1.5"/>
    <text x="650" y="295" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Account</text>
    
    <!-- Graph Relationships -->
    <line x1="230" y1="290" x2="320" y2="290" stroke="#388e3c" stroke-width="1.5"/>
    <text x="275" y="280" font-family="Arial, sans-serif" font-size="10" text-anchor="middle" fill="#333">MADE_AT</text>
    
    <line x1="380" y1="290" x2="470" y2="290" stroke="#388e3c" stroke-width="1.5"/>
    <text x="425" y="280" font-family="Arial, sans-serif" font-size="10" text-anchor="middle" fill="#333">BELONGS_TO</text>
    
    <line x1="530" y1="290" x2="620" y2="290" stroke="#388e3c" stroke-width="1.5"/>
    <text x="575" y="280" font-family="Arial, sans-serif" font-size="10" text-anchor="middle" fill="#333">HAS_ACCOUNT</text>
    
    <!-- Arrow -->
    <path d="M400,350 L400,380" stroke="#666" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
    
    <!-- AI Intelligence Layer -->
    <rect x="100" y="380" width="600" height="100" rx="8" ry="8" fill="#fff3e0" stroke="#ff9800" stroke-width="2"/>
    <text x="400" y="410" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#e65100">AI Intelligence Layer</text>
    
    <rect x="140" y="430" width="180" height="40" rx="5" ry="5" fill="#ffe0b2" stroke="#f57c00" stroke-width="1"/>
    <text x="230" y="455" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">LLM-Based Categorization</text>
    
    <rect x="480" y="430" width="180" height="40" rx="5" ry="5" fill="#ffe0b2" stroke="#f57c00" stroke-width="1"/>
    <text x="570" y="455" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">NL Query Agent</text>
    
    <!-- Arrow -->
    <path d="M400,480 L400,510" stroke="#666" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
    
    <!-- User Interface Layer -->
    <rect x="100" y="510" width="600" height="70" rx="8" ry="8" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
    <text x="400" y="545" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#4a148c">User Interface Layer</text>
    
    <text x="230" y="565" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Dashboard & Analytics</text>
    <text x="570" y="565" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Natural Language Interface</text>
    
    <!-- Arrowhead Marker -->
    <defs>
      <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
      </marker>
    </defs>
  </svg>
</div>




## 🚀 Project Vision

Managing personal finances shouldn't require spreadsheet expertise or hours of manual categorization. Financial Graph AI automates the tedious parts of financial tracking while providing intelligent insights about spending patterns that traditional finance apps miss.

This project explores the intersection of structured financial data and contextual AI understanding through:

1. Graph-based financial modeling that captures relationships between transactions, merchants, categories and accounts
2. LLM-powered smart categorization that understands merchant descriptions better than rule-based systems 
3. Natural language querying that lets users ask questions about their finances in plain English

## 🏗️ Architecture Overview

### Core Components

```
┌─────────────────┐     ┌───────────────────┐     ┌─────────────────┐
│  Data Ingestion │     │  AI Intelligence  │     │  User Interface │
│  & Processing   │────>│  & Analytics      │────>│  & Experience   │
└─────────────────┘     └───────────────────┘     └─────────────────┘
```

### Data Pipeline

1. **Upload Interface**
   - Support for CSV, Excel and PDF bank statements
   - File validation and schema detection
   - Secure storage with encryption at rest

2. **Data Processing**
   - Transaction normalization (dates, amounts, descriptions)
   - PDF parsing with OCR for scanned statements
   - Deduplication and reconciliation

3. **Graph Database Modeling**
   - **Nodes**: Transaction, Merchant, Category, Account, Tag
   - **Relationships**: 
     - Transaction → Merchant (MADE_AT)
     - Transaction → Category (BELONGS_TO)
     - Account → Account (TRANSFERRED_TO/FROM)
     - Transaction → Tag (HAS_TAG)

4. **AI-Powered Features**
   - Smart categorization with LLM few-shot prompting
   - Similarity detection using transaction embeddings
   - Natural language querying with an AI agent

5. **Analytics Engine**
   - Weekly spending analysis and aggregation
   - Category-based trend detection
   - Anomaly detection (unusual spending patterns)

## 💻 Technology Stack

- **Backend**: Python (FastAPI/Flask), NodeJS (Express)
- **Frontend**: React, Next.js, Tailwind CSS
- **Databases**: 
  - Neo4j (graph database)
  - PostgreSQL (relational data)
  - Vector database (Pinecone/Weaviate)
- **AI & ML**:
  - LLMs (OpenAI API or local models)
  - LangChain for agent implementation
  - Embeddings for transaction similarity
- **Visualization**: D3.js, recharts

## 🌟 Unique Features

### 1. Graph-Powered Financial Intelligence

Unlike traditional financial apps that use flat tables, our graph model captures the rich relationships between transactions, revealing patterns like:

- Recurring subscription detection across varied description formats
- Merchant consolidation (identifying when different transaction descriptions are the same merchant)
- Financial flow mapping between accounts

### 2. Context-Aware Transaction Categorization

We combine traditional rule-based categorization with LLM intelligence to achieve significantly higher accuracy:

- Few-shot prompting teaches the model about ambiguous merchant descriptions
- Transaction similarity through embeddings finds patterns a rule engine would miss
- User feedback loop continuously improves categorization accuracy

### 3. Natural Language Financial Assistant

Ask questions about your finances in plain English:

- "How much did I spend on restaurants last month compared to the month before?"
- "What are my top 5 largest recurring expenses?"
- "Did I pay my rent twice this month?"

## 🔒 Security & Privacy

This project takes a "privacy-first" approach:

- All financial data remains on your infrastructure
- Optional LLM processing with local models (no data sent to third parties)
- End-to-end encryption for sensitive financial information
- No data sharing or analytics beyond your personal instance

## 🛣️ Project Roadmap

### Phase 1: Core Infrastructure
- Basic data ingestion for CSV/Excel
- Initial graph database implementation
- Simple categorization with rules

### Phase 2: AI Enhancement
- LLM-powered smart categorization
- Embedding-based transaction similarity
- Basic analytics dashboard

### Phase 3: Advanced Features
- Natural language query agent
- PDF statement support with OCR
- Anomaly detection
- Advanced visualizations

### Phase 4: Optimization & Scale
- Performance improvements
- Multi-user support
- API for external integrations

## 📊 Performance Goals

- Process 5 years of transactions in under 60 seconds
- Achieve >90% categorization accuracy without user intervention
- Query response time <500ms for typical financial questions

## 🤝 Contributing

This project welcomes contributions! Whether you're interested in improving the AI components, enhancing the graph model, or building better visualizations, please see our [CONTRIBUTING.md](CONTRIBUTING.md) guide.

## 📄 License

Financial Graph AI is available under the MIT License. See [LICENSE](LICENSE) for more information.

---

*Built with ❤️ by [Your Name], combining the power of graph databases and modern AI to revolutionize personal finance.*