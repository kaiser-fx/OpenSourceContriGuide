# Open Source Contributor Platform

## Project Overview

Build a full-stack platform that helps developers discover suitable open-source GitHub issues based on their skills and experience.

The core problem is simple:

> A beginner developer wants to contribute to open source, but does not know which issues are suitable for them.

The MVP should solve this by allowing a user to create a skill profile, ingest public GitHub repositories/issues, and receive ranked issue recommendations.

The project should NOT become a GitHub analytics dashboard. The focus is contributor-to-issue matching.

---

## Project Vision

### MVP

```text
User
  ↓
Create account
  ↓
Select skills
  ↓
Platform has open-source projects/issues
  ↓
Recommendation engine matches skills to issues
  ↓
User sees ranked issues
  ↓
User opens the original GitHub issue
```

### Future Version

After the MVP is stable, add AI-powered features:

- AI issue explanation
- AI difficulty estimation
- Personalized learning paths
- Similar merged PR finder
- Semantic/embedding-based recommendations
- Contribution progress tracking

AI is an additional layer, not the foundation of the MVP.

---

# MVP Scope

## 1. Authentication

Implement:

- User registration
- User login
- Password hashing
- JWT authentication
- Protected endpoints
- Current-user endpoint

Suggested endpoints:

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

Do not implement GitHub OAuth in the MVP.

---

## 2. User Skill Profiles

Users should be able to select skills such as:

```text
Python
FastAPI
SQL
PostgreSQL
React
Docker
Machine Learning
Git
```

Users can have multiple skills.

Database relationship:

```text
User
  |
  +--- UserSkill --- Skill
```

Suggested endpoints:

```text
GET  /skills
POST /users/me/skills
GET  /users/me/skills
DELETE /users/me/skills/{skill_id}
```

---

## 3. GitHub Project and Issue Ingestion

Use the public GitHub REST API.

Start with a small curated set of open-source projects rather than trying to index GitHub.

Good initial projects could include:

- FastAPI
- OpenTelemetry Python
- MLflow
- Jupyter

The backend should fetch:

### Repository data

- Repository name
- Owner
- Description
- URL
- Primary language
- Stars

### Issue data

- GitHub issue ID
- Issue number
- Title
- Body
- Labels
- State
- URL
- Repository
- Created/updated timestamps

Only store useful open issues. Avoid pull requests unless required later.

Suggested internal service:

```text
github_service.py
```

Suggested endpoints:

```text
POST /github/sync/{owner}/{repo}
GET  /projects
GET  /projects/{project_id}
GET  /issues
GET  /issues/{issue_id}
```

The GitHub API should not be called directly from route handlers. Put external API logic in a service layer.

---

# 4. Recommendation Engine

This is the main feature of the MVP.

The first version should NOT use an LLM or a complicated ML model.

Use deterministic skill/metadata matching.

Example:

User:

```text
Python
FastAPI
SQL
```

Issue:

```text
Repository: FastAPI
Labels: python, good first issue, documentation
Language: Python
```

The system calculates a compatibility score.

Example:

```text
Issue A   95%
Issue B   82%
Issue C   67%
```

Return the highest-ranked issues.

A simple first scoring system can consider:

- Skill/label overlap
- Repository language vs user skills
- Repository technology
- `good first issue` label
- `help wanted` label
- Issue difficulty if available

Keep the scoring logic isolated in something like:

```text
recommendation_service.py
```

Suggested endpoint:

```text
GET /recommendations
```

Example response:

```json
{
  "recommendations": [
    {
      "issue_id": 42,
      "score": 0.95,
      "reason": "Matches Python and FastAPI skills"
    }
  ]
}
```

The recommendation algorithm should be easy to replace later with embeddings/ML.

---

# 5. Dashboard

The user should have a simple dashboard showing:

```text
Welcome, <username>

Your Skills
[Python] [FastAPI] [SQL]

Recommended Issues

1. Fix authentication documentation
   FastAPI
   Python
   Good First Issue
   Match: 95%

2. Improve SQL example
   Python
   SQL
   Match: 87%

3. Update API documentation
   FastAPI
   Match: 81%
```

Each issue should have:

- Title
- Repository
- Labels
- Match score
- Short reason for recommendation
- Link to original GitHub issue

Do not build complicated analytics/charts in the MVP.

---

# Tech Stack

## Frontend

- React
- TypeScript
- Tailwind CSS
- TanStack Query

The frontend should consume the FastAPI REST API.

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

## Database

- PostgreSQL

## Authentication

- JWT
- Password hashing with a modern password hashing library

## External API

- GitHub REST API

## Testing

- pytest
- FastAPI TestClient/httpx as appropriate

## Development

- Git
- GitHub
- `.env` for secrets/configuration

Docker and CI/CD can be added after the MVP.

---

# Suggested Architecture

```text
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │ TypeScript + Tailwind│
                    └──────────┬──────────┘
                               │
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend   │
                    ├─────────────────────┤
                    │ Auth Service         │
                    │ User/Skill Service   │
                    │ GitHub Service       │
                    │ Recommendation      │
                    │ Service              │
                    └───────┬───────┬─────┘
                            │       │
                 SQLAlchemy │       │ GitHub REST API
                            ▼       ▼
                    ┌──────────┐  ┌──────────┐
                    │PostgreSQL│  │  GitHub  │
                    └──────────┘  └──────────┘
```

---

# Backend Project Structure

Use a clean but not over-engineered structure:

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── database.py
│   │   └── models/
│   ├── schemas/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── skills.py
│   │   ├── projects.py
│   │   ├── issues.py
│   │   └── recommendations.py
│   ├── services/
│   │   ├── github_service.py
│   │   └── recommendation_service.py
│   └── dependencies/
├── alembic/
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

Do not create unnecessary microservices.

This should be a modular monolith.

---

# Initial Database Schema

Keep the MVP database small.

## users

```text
id
username
email
hashed_password
created_at
```

## skills

```text
id
name
```

## user_skills

```text
user_id
skill_id
```

## projects

```text
id
github_id
owner
name
description
github_url
language
stars
updated_at
```

## issues

```text
id
github_id
number
project_id
title
body
state
url
labels
created_at
updated_at
```

The exact schema can be refined during implementation.

---

# Development Phases

## Phase 1: Project Setup

Set up:

- Git repository
- Python environment
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Configuration management
- Basic application structure

Milestone:

```text
FastAPI runs
+
PostgreSQL connects
+
Alembic migration works
```

---

## Phase 2: Database Models

Implement:

- User
- Skill
- UserSkill
- Project
- Issue

Create migrations.

Milestone:

```text
All MVP tables exist in PostgreSQL.
```

---

## Phase 3: Authentication

Implement:

- Register
- Login
- JWT
- Password hashing
- `/auth/me`

Milestone:

```text
User can register → login → receive JWT → access protected endpoint.
```

---

## Phase 4: Skills

Implement skill CRUD/read operations and user skill assignment.

Milestone:

```text
User can create a skill profile.
```

---

## Phase 5: GitHub Integration

Implement the GitHub service.

Start by manually syncing a small number of repositories.

Milestone:

```text
GitHub repository
↓
GitHub API
↓
FastAPI
↓
PostgreSQL
↓
Issues available in application
```

---

## Phase 6: Recommendation Engine

Implement deterministic matching.

Milestone:

```text
User skills
+
Issue metadata
↓
Scoring algorithm
↓
Ranked recommendations
```

This is the MVP's most important phase.

---

## Phase 7: Frontend

Build:

- Login
- Register
- Skill selection
- Dashboard
- Issue list
- Issue detail page

Milestone:

```text
A real user can use the entire MVP without Swagger.
```

---

## Phase 8: Testing and Polish

Add:

- Unit tests
- API tests
- Validation
- Error handling
- Loading/error states
- Pagination where needed
- README
- Screenshots

Milestone:

```text
MVP is stable and demo-ready.
```

---

# Explicitly Out of MVP

Do NOT implement these before the MVP works:

- GitHub OAuth
- AI issue explanations
- Gemini/OpenAI integration
- Ollama
- RAG
- Vector database
- Semantic search
- Similar PR finder
- Redis
- Celery
- Microservices
- Complex analytics
- Recommendation ML model
- Mobile app

These belong to later versions.

---

# Version 2: AI/ML Layer

Once the MVP works, add the interesting AI features.

## Semantic Recommendations

Replace/augment keyword matching with:

```text
Issue text
    ↓
Sentence Transformer
    ↓
Embedding
    ↓
Similarity with user profile
    ↓
Ranked issues
```

A lightweight model such as `all-MiniLM-L6-v2` can be used locally.

Use cosine similarity or another appropriate similarity metric.

---

## AI Issue Explanation

On an issue page:

```text
Explain this issue
```

Output:

```text
Summary
Required skills
What the issue is asking for
Likely files/components involved
Estimated difficulty
Suggested starting point
```

Prefer a local model through Ollama or a free/low-cost API for development.

Do not make the core product dependent on a paid LLM API.

---

## AI Learning Path

Given an issue:

```text
Issue
↓
Required concepts
↓
Learning resources
↓
Suggested preparation steps
```

---

## Similar PR Finder

Use embeddings to find related merged pull requests.

```text
Issue
↓
Embedding
↓
Vector similarity
↓
Similar merged PRs
```

This can become a major interview discussion point.

---

# Version 3: Contribution Tracking

Add:

```text
Interested
Working
PR Submitted
PR Merged
```

Allow users to track issues they are attempting.

Potential future GitHub integration can automatically detect contribution progress.

---

# Important Product Principle

Do not turn this into:

```text
GitHub analytics dashboard
```

Avoid making repository stars, commit graphs, contribution heatmaps, and follower counts the central product.

The core value proposition is:

> Help developers find and understand open-source issues that they are realistically capable of contributing to.

---

# Interview Hook

The project should eventually be explainable as:

> "I built a platform that matches developers with open-source issues based on their skills. It integrates GitHub's API to ingest real issues and repositories, uses a recommendation engine to rank suitable contributions, and later adds semantic search and AI-powered issue explanations to reduce the barrier to making a first contribution."

This gives interview discussion around:

- FastAPI
- REST API design
- PostgreSQL
- SQLAlchemy
- JWT
- Third-party API integration
- Recommendation systems
- Embeddings
- Vector similarity
- LLM integration
- System design

---

# Coding Guidelines for Antigravity/Codex

1. Build incrementally.
2. Do not implement future features unless explicitly requested.
3. Do not over-engineer the MVP.
4. Prefer a modular monolith.
5. Keep business logic out of route handlers.
6. Use SQLAlchemy ORM properly.
7. Use Alembic for schema changes.
8. Never hardcode secrets.
9. Use environment variables.
10. Validate external GitHub API responses.
11. Handle GitHub rate limits and API errors gracefully.
12. Write tests for important business logic.
13. Keep recommendation scoring isolated so it can later be replaced by ML.
14. Use type hints throughout Python code.
15. Keep functions focused and reasonably small.
16. Do not add Redis, Celery, Docker, vector databases, or LLM providers prematurely.
17. Update the README as major functionality is completed.

---

# Definition of Done for MVP

The MVP is complete when:

- A user can register.
- A user can log in.
- JWT-protected endpoints work.
- A user can select skills.
- The system has real GitHub repositories.
- The system has real open issues.
- Issues are stored in PostgreSQL.
- The recommendation engine ranks issues based on user skills.
- The frontend displays recommendations.
- Users can open the original GitHub issue.
- Core functionality has tests.
- The project can be demonstrated end-to-end.

The AI layer should only begin after all of the above works.

---

# First Task

Start by creating the backend foundation only.

Implement:

```text
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Environment configuration
Basic health endpoint
```

Do NOT implement authentication, GitHub integration, frontend, AI, or recommendations in the first task.

The first successful milestone should be:

```text
GET /health
        ↓
{"status": "ok"}
        ↓
FastAPI
        ↓
PostgreSQL connection verified
```

Then proceed phase by phase.
