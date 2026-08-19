from enum import Enum
from pydantic import BaseModel, HttpUrl, EmailStr, Field
from typing import Annotated, List
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


class ExperienceLevel(str, Enum):
    NEVER_CONTRIBUTED = "Never Contributed"
    KNOW_GIT = "Know git"
    PR_BEFORE = "Make PRs before"


class ContributionGoal(str, Enum):
    FIRST_PR = "First PR"
    BUILD_PORTFOLIO = "Build Portfolio"
    LEARN_NEW_TECH = "Learn New Tech"
    MENTORSHIP = "Mentorship"


class ContributionType(str, Enum):
    DOCUMENTATION = "Documentation"
    CODE = "Code"


class DomainInterest(str, Enum):
    WEB_DEV = "Web Development"
    AI_ML = "AI / Machine Learning"
    DEVOPS = "DevOps & Cloud"
    MOBILE = "Mobile App Development"
    SYSTEMS = "Systems & CLI Tools"
    CYBERSECURITY = "Cybersecurity"


class ProgrammingLanguage(str, Enum):
    # Mainstream & Web
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    TYPESCRIPT = "TypeScript"
    JAVA = "Java"
    CPP = "C++"
    C = "C"
    CSHARP = "C#"
    GO = "Go"
    RUST = "Rust"
    RUBY = "Ruby"
    PHP = "PHP"
    SWIFT = "Swift"
    KOTLIN = "Kotlin"
    DART = "Dart"
    R = "R"
    SOLIDITY = "Solidity"
    SHELL = "Shell"
    HTML = "HTML"
    CSS = "CSS"
    SQL = "SQL"


class FrameworkOrLibrary(str, Enum):
    # Frontend Frameworks & UI
    REACT = "React"
    NEXTJS = "Next.js"
    VUE = "Vue.js"
    NUXTJS = "Nuxt.js"
    SVELTE = "Svelte"
    SVELTEKIT = "SvelteKit"
    ANGULAR = "Angular"
    SOLIDJS = "SolidJS"
    ASTRO = "Astro"
    REMIX = "Remix"
    TAILWIND = "Tailwind CSS"
    BOOTSTRAP = "Bootstrap"
    MUI = "Material UI (MUI)"
    SHADCN = "shadcn/ui"

    # Backend Frameworks & Runtimes
    NODEJS = "Node.js"
    EXPRESS = "Express.js"
    NESTJS = "NestJS"
    FASTAPI = "FastAPI"
    DJANGO = "Django"
    FLASK = "Flask"
    SPRING_BOOT = "Spring Boot"
    RAILS = "Ruby on Rails"
    ASPNET_CORE = "ASP.NET Core"
    LARAVEL = "Laravel"
    GIN = "Gin (Go)"
    FIBER = "Fiber (Go)"
    ACTIX_WEB = "Actix Web (Rust)"
    AXUM = "Axum (Rust)"

    # AI / Machine Learning / Data Science
    PYTORCH = "PyTorch"
    TENSORFLOW = "TensorFlow"
    KERAS = "Keras"
    SCIKIT_LEARN = "Scikit-Learn"
    PANDAS = "Pandas"
    NUMPY = "NumPy"
    HUGGING_FACE = "Hugging Face / Transformers"
    LANGCHAIN = "LangChain"
    LLAMA_INDEX = "LlamaIndex"
    OPENCV = "OpenCV"

    # Mobile & Desktop
    REACT_NATIVE = "React Native"
    FLUTTER = "Flutter"
    IONIC = "Ionic"
    ELECTRON = "Electron"
    TAURI = "Tauri"

    # Databases, ORMs & Caching
    POSTGRESQL = "PostgreSQL"
    MONGODB = "MongoDB"
    REDIS = "Redis"
    PRISMA = "Prisma"
    SQLALCHEMY = "SQLAlchemy"
    DRIZZLE = "Drizzle ORM"

    # DevOps, Cloud & CI/CD
    DOCKER = "Docker"
    KUBERNETES = "Kubernetes"
    TERRAFORM = "Terraform"
    ANSIBLE = "Ansible"
    GITHUB_ACTIONS = "GitHub Actions"
    GRAPHQL = "GraphQL"
    GRPC = "gRPC"

    # Testing Frameworks
    PYTEST = "Pytest"
    JEST = "Jest"
    VITEST = "Vitest"
    PLAYWRIGHT = "Playwright"
    CYPRESS = "Cypress"


class QuestionaireSubmittion(BaseModel):
    experience_level: Annotated[ExperienceLevel, Field(..., description='Experience level of the user')]
    contribution_goal: Annotated[ContributionGoal, Field(..., description='Contribution goal of the user')]
    contribution_type: Annotated[ContributionType, Field(..., description='Contribution type of the user')]
    domain_interests: Annotated[List[DomainInterest], Field(..., description='Domain interests of the user')]
    target_languages: Annotated[List[ProgrammingLanguage], Field(..., min_length=1, description='Target languages of the user')]
    target_frameworks: Annotated[List[FrameworkOrLibrary], Field(default_factory=list, description='Target frameworks and libraries')]
