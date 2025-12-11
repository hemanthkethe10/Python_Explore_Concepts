# Python Examples

A collection of Python examples demonstrating various AI/ML integrations, including LLM observability, vector databases, and agent workflows.

## Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Project Structure

```
.
├── requirements.txt          # Project dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── .env.example             # Environment variables template
│
├── langfuse_example.py      # Langfuse observability example
├── opik_*.py                # Opik prompt optimization examples
├── lang_graph_test.py       # LangGraph workflow example
├── human_in_middle.py       # Human-in-the-loop agent
│
├── mongo.py                 # MongoDB integration
├── pinecone_test.py         # Pinecone vector DB example
│
├── async_test.py            # Async HTTP requests example
├── chunking.py              # Text chunking utilities
├── readExcel.py             # Pandas CSV/Excel reading
│
└── aws/                     # AWS-related utilities
    └── encode.py            # Base64 encoding utilities
```

## Examples

### LLM Observability

- **langfuse_example.py** - Demonstrates LLM tracing with Langfuse
- **opik_simple_example.py** - Simple prompt optimization with Opik

### Agent Workflows

- **lang_graph_test.py** - State machine workflow with LangGraph
- **human_in_middle.py** - Human-in-the-loop pattern for agent verification

### Data & Databases

- **mongo.py** - MongoDB document operations
- **pinecone_test.py** - Vector upsert/query with Pinecone

## Environment Variables

Required API keys (set in `.env` file):

```bash
# OpenAI
OPENAI_API_KEY=your-openai-key

# Langfuse (optional)
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_HOST=https://us.cloud.langfuse.com

# Pinecone (optional)
PINECONE_API_KEY=your-pinecone-key

# MongoDB (optional)
MONGODB_URI=your-mongodb-uri
```

## Usage

Run any example script:

```bash
python langfuse_example.py
python opik_simple_example.py
python lang_graph_test.py
```

## License

MIT
