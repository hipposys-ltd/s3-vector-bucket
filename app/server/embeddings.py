from fastapi import APIRouter, Request, File, UploadFile
from typing import Annotated
import os
from app.vector import VectorDB
from typing import List
from pydantic import BaseModel
import shutil

embeddings_router = APIRouter()


@embeddings_router.get("/")
async def new_chat(request: Request):
    """Create a new chat session."""
    return {'results': 'ok'}


@embeddings_router.get("/list_vectors/")
async def list_vectors():
    return VectorDB().list_vectors()


class DeleteVectorsRequest(BaseModel):
    vectors_to_delete: List[str]


@embeddings_router.delete("/delete_vectors/")
async def delete_vectors(request: DeleteVectorsRequest):
    VectorDB().delete_vectors(request.vectors_to_delete)
    return {'results': 'ok'}


@embeddings_router.post("/upload_file/")
async def upload_file(file: Annotated[UploadFile, File()]):
    path = 'temp.pdf'
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return VectorDB().upload_file(path, file.filename)
