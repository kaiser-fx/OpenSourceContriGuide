from pydantic import BaseModel, HttpUrl, EmailStr, Field
from typing import Annotated
from uuid import UUID

class UserProfileInfo(BaseModel):
    first_name: Annotated[str, Field(min_length=1, max_length=50, description='First name of the user')]
    last_name: Annotated[str, Field(min_length=1, max_length=50, description='Last name of the user')]
    email: Annotated[EmailStr, Field(..., description='Email of the user')]
    github_url: Annotated[HttpUrl, Field(..., description='GitHub profile Link of the user')]
    linkedin_url: Annotated[HttpUrl, Field(..., description='LinkedIn profile Link of the user')]
    leetcode_url: Annotated[HttpUrl | None, Field(default=None, description='LeetCode profile Link of the user')] = None
    resume_id: Annotated[UUID | None, Field(default=None, description='Resume ID')] = None
    resume_filename: Annotated[str | None, Field(default=None, description='Resume filename')] = None


class TestGithubProfile(BaseModel):
    github_link: HttpUrl

    