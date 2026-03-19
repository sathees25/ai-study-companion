from fastapi import APIRouter,UploadFile,File,HTTPException
from pydantic import BaseModel
from services.rag_service import process_pdf, rag_query
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR,exist_ok=True)

UPLOADED_FILE = os.path.join(UPLOAD_DIR,"current.pdf")

@router.post("/upload")
async def upload_pdf(file: UploadFile =File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400,detail="only pdf files are supported")

    with open(UPLOADED_FILE,'wb') as buffer:
        shutil.copyfileobj(file.file,buffer)

    try:
        num_chunks = process_pdf(UPLOADED_FILE)
    except Exception as e:
        raise HTTPException(status_code=500,detail= f"Failed to process pdf str{e}")
    
    return {
        "filename": file.filename,
        "chunks_indexed": num_chunks,
        "message": "PDF uploaded and indexed. Ready to query.",
    }


class RagRequest(BaseModel):
    query:str


@router.post("/upload/query")
async def query_pdf(req:RagRequest):
    
    try:
        answer = rag_query(req.query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
 
    return {"question": req.query, "answer": answer}

