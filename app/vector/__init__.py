import os
import boto3
import json
from langchain_community.document_loaders import PyPDFLoader
from app.indexing.text.base import BaseTextIndexing
from app.indexing.metadata import DocumentMetadata
from datetime import datetime
import uuid


class VectorDB:
    def __init__(self):
        self.bucket = os.environ.get('bucket')
        self.index = os.environ.get('index')
        self.bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
        self.s3vectors = boto3.client('s3vectors', region_name='us-east-1')
        self.embedding_model = os.environ.get('embedding_model',
                                              'amazon.titan-embed-text-v2:0')

    def search(self, input_text):
        # Create the JSON request for the model.
        request = json.dumps({"inputText": input_text})
        # Invoke the model with the request and the model ID, e.g., Titan Text Embeddings V2. 
        response = self.bedrock.invoke_model(modelId=self.embedding_model,
                                             body=request)
        # Decode the model's native response body.
        model_response = json.loads(response["body"].read())
        # Extract and print the generated embedding and the input text token count.
        embedding = model_response["embedding"]
        # Performa a similarity query. You can also optionally use a filter in your query
        query = self.s3vectors.query_vectors(
            vectorBucketName=self.bucket,
            indexName=self.index,
            queryVector={"float32": embedding},
            topK=3,
            # filter={"genre": "scifi"},
            returnDistance=True,
            returnMetadata=True
        )
        return query["vectors"]

    def list_vectors(self):
        query = self.s3vectors.list_vectors(
            vectorBucketName=self.bucket,
            indexName=self.index,
            returnMetadata=True
        )
        return [{**vector['metadata'], **{'key': vector['key']}}
                for vector in query['vectors']]

    def delete_vectors(self, vector_keys: list):
        self.s3vectors.delete_vectors(
            vectorBucketName=self.bucket,
            indexName=self.index,
            keys=vector_keys
        )

    def upload_file(self, file_path: str, file_name: str):
        loader = PyPDFLoader(file_path)
        docs = [p for p in loader.lazy_load()]
        splits = BaseTextIndexing().split(text=docs, metadata=DocumentMetadata(
            # In our case, the filename is unique, but you may want to choose a different ID and Name, in other cases.
            source_id='manually_uploaded',
            source_name=file_name,
            modified_at=datetime.fromtimestamp(os.path.getmtime(file_path)),
        ))
        embeddings = []
        print(splits[0])
        for split in splits:
            body = json.dumps({
                "inputText": split.page_content
            })
            # Call Bedrock's embedding API
            response = self.bedrock.invoke_model(
                modelId=self.embedding_model,
                body=body)
            response_body = json.loads(response['body'].read())
            embedding = response_body['embedding']
            embedding_meta = {
                "key": str(uuid.uuid4()),
                "data": {"float32": embedding},
                "metadata": {
                    "source_name": split.metadata['source_name'],
                    "modified_at": split.metadata['modified_at'],
                    "created_at": split.metadata['payload']['creationdate'],
                    "source": split.metadata['payload']['source'],
                    "page_label": split.metadata['payload']['page_label'],
                    "title": split.metadata['payload']['title'],
                    "subject": split.metadata['payload']['subject'],
                    "content": split.page_content}}
            embeddings.append(embedding_meta)
        self.s3vectors.put_vectors(
            vectorBucketName=self.bucket,
            indexName=self.index,
            vectors=embeddings)
