# S3 Vector Bucket with LangChain Demo

A demonstration of using AWS S3 Vector Buckets as a vector store for RAG (Retrieval-Augmented Generation) systems with LangChain integration.

## Overview

This project shows how to:
- Store document embeddings in AWS S3 Vector Buckets
- Search vectors using semantic similarity
- Integrate with LangChain for RAG workflows
- Build a Streamlit interface for document management and chat

## Prerequisites

- AWS account with appropriate permissions
- Python 3.8+
- Docker and Docker Compose
- [just](https://github.com/casey/just) command runner (optional but recommended)

## AWS Setup

### 1. Create S3 Vector Bucket

1. Navigate to AWS S3 console
2. Select "Vector Buckets" from the left menu
3. Create a new vector bucket
4. Note the bucket name for configuration

### 2. Create Vector Index

1. In your vector bucket, create a new index
2. Set dimensions to `1024` (for Amazon Titan embeddings)
3. Choose `Cosine Similarity` as the similarity measure
4. Note the index name for configuration

## Local Setup

### 1. Clone and Setup

```bash
git clone https://github.com/ponderedw/s3-vector-bucket
cd s3-vector-bucket
cp template.env .env
```

### 2. Configure Environment

Edit `.env` file with your settings:

```env
DEPLOY_ENV='local'

# Postgres
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_DB='postgres'

# LLM Model (choose one)
LLM_MODEL_ID='bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0'  # For Bedrock
# LLM_MODEL_ID='anthropic:claude-3-5-sonnet-20241022'            # For Anthropic API
# LLM_MODEL_ID='openai:gpt-4'                                    # For OpenAI API

# Secrets (replace in production)
SECRET_KEY='ThisIsATempSecretForLocalEnvs.ReplaceInProd.'
FAST_API_ACCESS_SECRET_TOKEN='ThisIsATempAccessTokenForLocalEnvs.ReplaceInProd'

# AWS Credentials
AWS_ACCESS_KEY_ID='your-access-key'
AWS_SECRET_ACCESS_KEY='your-secret-key'
AWS_DEFAULT_REGION='us-east-1'

# API Keys (if not using Bedrock)
# ANTHROPIC_API_KEY='your-anthropic-key'
# OPENAI_API_KEY='your-openai-key'

# Vector Store Configuration
bucket='your-vector-bucket-name'
index='your-vector-index-name'

# Optional: Custom embedding model
# embedding_model='amazon.titan-embed-text-v2:0'
```

### 3. Download Sample Data

```bash
# Download NYC Planning dataset
wget https://ponder-public-assets.s3.us-east-1.amazonaws.com/newsletter-assets/NYC+Planning.zip
unzip "NYC+Planning.zip" -d data/
```

### 4. Run the Application

```bash
# Using just (recommended)
just all
```

## Usage

Open your browser and navigate to `http://localhost:8501`

### Available Tabs:

1. **Main** - Chat interface to query your vector store
2. **Load File** - Upload PDF documents to populate your vector index
3. **See Vectors** - View and manage stored embeddings

### Getting Started:

1. Go to the **Load File** tab
2. Upload PDF files from the `data/` folder
3. Wait for processing to complete
4. Check the **See Vectors** tab to see your uploaded data
5. Switch to the **Main** tab and try queries like:
   - "What are the changing conditions of the Special Hudson Yards District?"
   - "Tell me about NYC planning regulations"



## Key Features

### Vector Operations
- **Search**: Semantic similarity search using embeddings
- **Upload**: Process and store document embeddings
- **List**: View all stored vectors with metadata
- **Delete**: Remove individual vectors or entire documents

### LangChain Integration
```python
retriever = VectorDB()
tool = Tool(
    name="Data_Retriever",
    func=retriever.search,
    description="Searches S3 vector bucket for similar embeddings and returns matching results",
)
```


## Configuration Options

### Embedding Models
- Default: `amazon.titan-embed-text-v2:0` (1024 dimensions)
- Custom models can be specified in the `.env` file

### LLM Models
- Bedrock: `bedrock:model-id`
- Anthropic: `anthropic:model-name`
- OpenAI: `openai:model-name`


