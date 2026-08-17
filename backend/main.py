from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status

from app.models import UserProfileInfo

app = FastAPI()

UPLOAD_DIRECTORY = Path(__file__).parent / "uploads" / "resumes"
MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024
ALLOWED_RESUME_CONTENT_TYPES = {"application/pdf"}
ALLOWED_RESUME_SUFFIXES = {".pdf"}

@app.get("/")
def home():
    return {"message": "Hello Welcome to Open Source Contribution Guide"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/users/me/profile", response_model=UserProfileInfo, status_code=status.HTTP_201_CREATED)
async def create_profile(
    first_name: Annotated[str, Form(...)],
    last_name: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    github_url: Annotated[str, Form(...)],
    linkedin_url: Annotated[str, Form(...)],
    leetcode_url: Annotated[str | None, Form()] = None,
    resume: Annotated[UploadFile | None, File()] = None,
):
    resume_id = None
    resume_filename = None

    if resume is not None and resume.filename:
        # Validate file suffix
        suffix = Path(resume.filename).suffix.lower()
        if suffix not in ALLOWED_RESUME_SUFFIXES or resume.content_type not in ALLOWED_RESUME_CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only PDF files are allowed.",
            )

        content = await resume.read()
        if len(content) > MAX_RESUME_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume file size exceeds the 5MB limit.",
            )

        resume_id = uuid4()
        resume_filename = f"{resume_id}_{resume.filename}"
        UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
        file_path = UPLOAD_DIRECTORY / resume_filename
        file_path.write_bytes(content)

    return UserProfileInfo(
        first_name=first_name,
        last_name=last_name,
        email=email,
        github_url=github_url,
        linkedin_url=linkedin_url,
        leetcode_url=leetcode_url,
        resume_id=resume_id,
        resume_filename=resume_filename,
    )
