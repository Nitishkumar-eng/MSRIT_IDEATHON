import uvicorn
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import shutil

from parsers import get_parser
from engine import compare_documents

app = FastAPI(title="Multi-Format Document Compliance Analyzer")
templates = Jinja2Templates(directory="templates")

os.makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/analyze")
async def analyze_document(
    template_file: UploadFile = File(...),
    target_file: UploadFile = File(...)
):
    # Save files temporarily
    template_path = f"uploads/temp_template_{template_file.filename}"
    target_path = f"uploads/temp_target_{target_file.filename}"
    
    with open(template_path, "wb") as buffer:
        shutil.copyfileobj(template_file.file, buffer)
        
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(target_file.file, buffer)
        
    try:
        template_parser = get_parser(template_path)
        target_parser = get_parser(target_path)
        
        template_data = template_parser.parse(template_path)
        target_data = target_parser.parse(target_path)
        
        result = compare_documents(template_data, target_data)
    except Exception as e:
        result = {
            "overall_score": 0,
            "subscores": {"structure": 0, "order": 0, "formatting": 0},
            "issues": [f"Error processing files: {str(e)}"]
        }
    
    # Cleanup
    os.remove(template_path)
    os.remove(target_path)
    
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
