from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import uuid

from backend.services.pdf_service import extract_text_from_pdf, chunk_text
from backend.services.embedding_service import add_chunks_to_collection, query_collection, delete_collection
from backend.services.llm_service import ask_question, generate_summary

router = APIRouter()

class QuestionRequest(BaseModel):
    paper_id: str
    question: str

class DeleteRequest(BaseModel):
    paper_id: str

@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)

        if len(text.strip()) < 100:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        paper_id = str(uuid.uuid4()).replace('-', '')[:16]
        chunks = chunk_text(text)
        num_chunks = add_chunks_to_collection(paper_id, chunks)

        summary_raw = generate_summary(text)
        try:
            summary = json.loads(summary_raw)
        except:
            summary = {"title": file.filename, "summary": summary_raw, "key_findings": []}

        return JSONResponse({
            "paper_id": paper_id,
            "filename": file.filename,
            "num_chunks": num_chunks,
            "summary": summary
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
async def ask(request: QuestionRequest):
    try:
        relevant_chunks = query_collection(request.paper_id, request.question)
        context = "\n\n---\n\n".join(relevant_chunks)
        answer = ask_question(context, request.question)
        return JSONResponse({"answer": answer, "context_used": len(relevant_chunks)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
async def delete_paper(request: DeleteRequest):
    try:
        delete_collection(request.paper_id)
        return JSONResponse({"message": "Paper deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))