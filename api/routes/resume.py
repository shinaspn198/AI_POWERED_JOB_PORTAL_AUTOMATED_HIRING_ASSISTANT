from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from pydantic import BaseModel
from api.schemas import ResumeUploadResponse
import uuid

from parsers.resume_parser import parse_resume


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ==============================
# Resume Parse Request
# ==============================

class ResumeParseRequest(BaseModel):
    candidate_id: str


# ==============================
# Resume Upload API
# ==============================
@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(resume: UploadFile = File(...)):

    allowed_types = {
        "application/pdf": ".pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx"
    }

    if resume.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    candidate_id = f"CAND-{uuid.uuid4().hex[:8].upper()}"

    extension = allowed_types[resume.content_type]

    filename = f"{candidate_id}{extension}"

    file_path = UPLOAD_DIR / filename

    contents = await resume.read()

    with open(file_path, "wb") as file:
        file.write(contents)

    return {
        "candidate_id": candidate_id,
        "filename": resume.filename,
        "status": "uploaded",
        "message": "Resume uploaded successfully"
    }


# ==============================
# Resume Parsing API
# ==============================

@router.post("/parse")
async def parse_resume_api(request: ResumeParseRequest):

    candidate_id = request.candidate_id

    # Find uploaded resume
    matching_files = list(UPLOAD_DIR.glob(f"{candidate_id}.*"))

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="Resume not found for candidate"
        )

    resume_path = matching_files[0]

    try:
        # Use existing resume parser
        parsed_resume = parse_resume(str(resume_path))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Resume parsing failed: {str(e)}"
        )

    return {
    "candidate_id": candidate_id,
    "status": "parsed",
    "profile": {
        "name": parsed_resume.get("name", ""),
        "email": parsed_resume.get("email", ""),
        "phone": parsed_resume.get("phone", ""),
        "location": parsed_resume.get("location", ""),
        "summary": parsed_resume.get("summary", ""),
        "skills": parsed_resume.get("skills", []),
        "experience": parsed_resume.get("experience", []),
        "education": parsed_resume.get("education", []),
        "projects": parsed_resume.get("projects", []),
        "certifications": parsed_resume.get("certifications", []),
        "languages": parsed_resume.get("languages", [])
    }
}