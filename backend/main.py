from pathlib import Path
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from dotenv import load_dotenv

from app.models import UserProfileInfo, TestGithubProfile

load_dotenv()

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


@app.post("/skill-dashboard")
def get_skill_dashboard(profile_link: TestGithubProfile):
    #Extracts Username
    username = profile_link.github_link.path.strip("/")
    headers = {"User-Agent": "OpenSourceContriGuide"} #User-Agent is mandatary for github api

    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    try:
        #User info
        req_profile = Request(f"https://api.github.com/users/{username}", headers=headers)
        with urlopen(req_profile) as response:
            profile_data = json.loads(response.read().decode())

        #User Repos Info
        req_repos = Request(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
        with urlopen(req_repos) as response:
            repos_data = json.loads(response.read().decode())

    except HTTPError as e:
        if e.code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"GitHub user '{username}' not found.")
        elif e.code == 403:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="GitHub rate limit reached. Add a GITHUB_TOKEN in .env for 5,000 req/hr.")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"GitHub error: {e.reason}")

    languages = sorted(list({
        repo["language"] 
        for repo in repos_data 
        if repo.get("language")}))
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)


    dashboard_data = {
        "username": username,
        "name": profile_data.get("name"),
        "bio": profile_data.get("bio"),
        #"avatar_url": profile_data.get("avatar_url"),
        "public_repos": profile_data.get("public_repos"),
        #"followers": profile_data.get("followers"),
        #"following": profile_data.get("following"),
        "total_stars": total_stars,
        "languages": languages,
        "repositories": [
            {
                "name": repo.get("name"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "url": repo.get("html_url"),
            }
            for repo in repos_data
        ],
    }


    print("Dashboard Data:", json.dumps(dashboard_data, indent=2))
    print(languages)

    return dashboard_data

@app.post("skills/questionaire",status_code=status.HTTP_200_OK)
def submit_questionaire():

    pass