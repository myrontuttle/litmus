# Test-Driven Development & Code Generation Guide

Practical TDD patterns and code generation techniques for this vibetuner + FastAPI + MongoDB stack.

---

## Part 1: Test-Driven Development (TDD) Workflow

### The TDD Cycle: Red → Green → Refactor

#### Step 1: RED (Write Failing Test)

Before writing ANY implementation code, write a test that fails.

```python
# tests/test_user_service.py
import pytest
from app.services.user import create_user, get_user_by_email
from app.models import User

@pytest.mark.asyncio
async def test_create_user_stores_email_and_password_hash():
    """Creating a user should hash the password."""
    user = await create_user(
        email="alice@example.com",
        password="securepass123"
    )

    # Verify user was created
    assert user.email == "alice@example.com"
    assert user.id is not None

    # Verify password is hashed (not stored in plaintext)
    assert user.password_hash is not None
    assert user.password_hash != "securepass123"
    assert user.password_hash.startswith("$2b")  # bcrypt prefix
```

Run the test to confirm it fails:

```bash
uv run pytest tests/test_user_service.py::test_create_user_stores_email_and_password_hash -v
# FAILED - ModuleNotFoundError: No module named 'app.services.user'
```

**This is OK!** The test failure is expected and guides what to build.

#### Step 2: GREEN (Write Minimal Implementation)

Write the minimum code to make the test pass.

```python
# src/app/services/user.py
import bcrypt
from app.models import User

async def create_user(email: str, password: str) -> User:
    """Create a new user with hashed password."""
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Create user
    user = User(
        email=email,
        password_hash=password_hash.decode()
    )
    await user.insert()
    return user

async def get_user_by_email(email: str) -> User | None:
    """Get user by email, or None if not found."""
    return await User.find_one(User.email == email)
```

Run the test:

```bash
uv run pytest tests/test_user_service.py::test_create_user_stores_email_and_password_hash -v
# PASSED ✅
```

#### Step 3: REFACTOR (Improve Code)

Now that the test passes, improve the code without breaking the test.

```python
# src/app/services/user.py
import bcrypt
from beanie.operators import Eq
from app.models import User
from app.exceptions import UserExistsError

async def create_user(email: str, password: str) -> User:
    """
    Create a new user with hashed password.

    Args:
        email: User's email address (must be unique)
        password: Plain text password (will be hashed)

    Returns:
        Created User object

    Raises:
        UserExistsError: If email already exists
    """
    # Check if user already exists
    existing = await User.find_one(Eq(User.email, email))
    if existing:
        raise UserExistsError(f"User with email {email} already exists")

    # Hash password with bcrypt
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Create and save user
    user = User(
        email=email,
        password_hash=password_hash.decode()
    )
    await user.insert()
    return user
```

The test still passes, but now the code is more robust. ✅

---

### Writing Comprehensive Test Coverage

#### Model Tests

Test data validation and constraints:

```python
# tests/test_models/test_user.py
import pytest
from app.models import User

@pytest.mark.asyncio
async def test_user_model_with_required_fields():
    """User can be created with required fields."""
    user = User(email="test@example.com", password_hash="$2b$hashed")
    assert user.email == "test@example.com"
    assert user.password_hash == "$2b$hashed"

@pytest.mark.asyncio 
async def test_user_model_email_validation():
    """User email must be valid format."""
    with pytest.raises(ValueError):
        User(email="invalid-email", password_hash="hash")

@pytest.mark.asyncio
async def test_user_model_timestamps():
    """User should have created_at timestamp."""
    user = User(email="test@example.com", password_hash="hash")
    assert user.created_at is not None
```

#### Service Tests

Test business logic:

```python
# tests/test_services/test_user_service.py
import pytest
from app.services.user import create_user, authenticate_user
from app.exceptions import UserExistsError

@pytest.mark.asyncio
async def test_create_user_success():
    """User creation should succeed with valid data."""
    user = await create_user(email="new@example.com", password="pass123")
    assert user.id is not None
    assert user.email == "new@example.com"

@pytest.mark.asyncio
async def test_create_user_duplicate_email_fails():
    """Creating user with duplicate email should raise error."""
    await create_user(email="taken@example.com", password="pass123")
    with pytest.raises(UserExistsError):
        await create_user(email="taken@example.com", password="other")

@pytest.mark.asyncio
async def test_authenticate_user_success():
    """Authentication should succeed with correct password."""
    await create_user(email="auth@example.com", password="correct123")
    user = await authenticate_user("auth@example.com", "correct123")
    assert user is not None
    assert user.email == "auth@example.com"

@pytest.mark.asyncio
async def test_authenticate_user_wrong_password():
    """Authentication should fail with wrong password."""
    await create_user(email="auth2@example.com", password="correct123")
    user = await authenticate_user("auth2@example.com", "wrong456")
    assert user is None

@pytest.mark.asyncio
async def test_authenticate_user_not_found():
    """Authentication should fail if user doesn't exist."""
    user = await authenticate_user("nonexistent@example.com", "anypass")
    assert user is None
```

#### Route Tests

Test HTTP endpoints:

```python
# tests/test_routes/test_auth_routes.py
import pytest
from fastapi.testclient import TestClient
from app.frontend.routes import app

@pytest.mark.asyncio
async def test_signup_with_valid_data():
    """POST /auth/signup should create user and return 201."""
    client = TestClient(app)
    response = client.post("/auth/signup", json={
        "email": "new@example.com",
        "password": "secure123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "new@example.com"

@pytest.mark.asyncio
async def test_signup_with_invalid_email():
    """POST /auth/signup should reject invalid email format."""
    client = TestClient(app)
    response = client.post("/auth/signup", json={
        "email": "not-an-email",
        "password": "secure123"
    })
    assert response.status_code == 400
    assert "email" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_signup_with_weak_password():
    """POST /auth/signup should reject weak passwords."""
    client = TestClient(app)
    response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "123"  # Too short
    })
    assert response.status_code == 400
    assert "password" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_signup_duplicate_email():
    """POST /auth/signup should reject duplicate email."""
    client = TestClient(app)

    # Create first user
    response1 = client.post("/auth/signup", json={
        "email": "taken@example.com",
        "password": "secure123"
    })
    assert response1.status_code == 201

    # Try to create with same email
    response2 = client.post("/auth/signup", json={
        "email": "taken@example.com",
        "password": "other123"
    })
    assert response2.status_code == 409  # Conflict
```

#### Integration Tests

Test complete workflows:

```python
# tests/test_integration/test_auth_flow.py
import pytest
from httpx import AsyncClient
from app.models import User
from app.frontend.app import app

@pytest.mark.asyncio
async def test_complete_auth_flow():
    """Test signup → login → access protected route."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 1. Sign up
        signup_resp = await client.post("/auth/signup", json={
            "email": "flow@example.com",
            "password": "password123"
        })
        assert signup_resp.status_code == 201
        user_id = signup_resp.json()["id"]

        # 2. Login
        login_resp = await client.post("/auth/login", json={
            "email": "flow@example.com",
            "password": "password123"
        })
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]

        # 3. Access protected route with token
        headers = {"Authorization": f"Bearer {token}"}
        profile_resp = await client.get("/user/profile", headers=headers)
        assert profile_resp.status_code == 200
        assert profile_resp.json()["email"] == "flow@example.com"
```

---

### TDD Best Practices for This Stack

#### 1. Test Database Isolation

Always use test database, not production:

```python
# tests/conftest.py
import pytest
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient
from app.models import User, Post

@pytest.fixture
async def test_db():
    """Provide isolated test database."""
    client = AsyncMongoMockClient()
    db = client.test_db

    # Initialize beanie with test models
    await init_beanie(db, models=[User, Post])

    yield db

    # Cleanup
    await client.close()

@pytest.fixture
async def test_user(test_db):
    """Provide a test user."""
    user = User(email="test@example.com", password_hash="hashed")
    await user.insert()
    return user
```

#### 2. Mock External Services

Don't call real email/payment services in tests:

```python
# tests/test_services/test_notifications.py
import pytest
from unittest.mock import AsyncMock, patch
from app.services.notifications import send_welcome_email

@pytest.mark.asyncio
async def test_send_welcome_email():
    """Welcome email is sent after signup."""
    with patch("app.services.email.send_email", new_callable=AsyncMock) as mock:
        await send_welcome_email("alice@example.com")

        # Verify email service was called
        mock.assert_called_once()
        call_args = mock.call_args
        assert "alice@example.com" in call_args[1]["to_email"]
        assert "Welcome" in call_args[1]["subject"]
```

#### 3. Test Async Code Properly

Use `@pytest.mark.asyncio`:

```python
# ✅ GOOD - Async test
@pytest.mark.asyncio
async def test_async_operation():
    result = await some_async_function()
    assert result == expected

# ❌ BAD - Sync test, won't work
def test_async_operation():
    result = await some_async_function()  # Error!
```

#### 4. Use Fixtures for Setup

```python
# ✅ GOOD - Reusable fixture
@pytest.fixture
async def admin_user():
    user = User(email="admin@example.com", password_hash="hash", is_admin=True)
    await user.insert()
    return user

@pytest.mark.asyncio
async def test_admin_can_delete_posts(admin_user):
    # admin_user is automatically set up
    response = await client.delete(f"/posts/123", headers=auth(admin_user))
    assert response.status_code == 204

# ❌ BAD - Repeated setup
@pytest.mark.asyncio
async def test_admin_can_delete_posts():
    # This admin setup is repeated everywhere
    user = User(email="admin@example.com", password_hash="hash", is_admin=True)
    await user.insert()
    response = await client.delete(f"/posts/123", headers=auth(user))
    assert response.status_code == 204
```

#### 5. Test One Thing Per Test

```python
# ✅ GOOD - Single concept
@pytest.mark.asyncio
async def test_password_must_be_hashed():
    user = User(email="test@example.com", password_hash="$2b$hashed")
    assert user.password_hash.startswith("$2b$")

# ❌ BAD - Multiple concepts
@pytest.mark.asyncio
async def test_user_creation():  # Too vague
    user = User(email="test@example.com", password_hash="hash")
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.password_hash is not None  # What are we testing?
```

---

## Part 2: Code Generation Best Practices

### Pattern 1: CRUD Factory (Zero-to-API)

Generate full CRUD endpoints automatically:

```python
# src/app/frontend/routes/posts.py
from vibetuner.crud import create_crud_routes
from app.models import Post

# Generate REST endpoints with one call
post_routes = create_crud_routes(
    Post,
    prefix="/api/posts",
    tags=["posts"],
    sortable_fields=["created_at", "title"],
    filterable_fields=["status"],
    searchable_fields=["title", "content"],
    page_size=20,
)

# Generated endpoints:
# GET    /api/posts              (list with pagination, filtering, sorting, search)
# POST   /api/posts              (create)
# GET    /api/posts/{id}         (read)
# PATCH  /api/posts/{id}         (update)
# DELETE /api/posts/{id}         (delete)
```

**This generates 5 fully-functional endpoints** with:

- ✅ Pagination
- ✅ Filtering
- ✅ Sorting
- ✅ Full-text search
- ✅ Input validation
- ✅ Error handling
- ✅ OpenAPI docs

### Pattern 2: Model-Driven Routes

Define models, generate routes automatically:

```python
# src/app/models/article.py
from beanie import Document
from pydantic import Field, EmailStr
from vibetuner.models.mixins import TimeStampMixin

class Article(Document, TimeStampMixin):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=10)
    author_email: EmailStr
    tags: list[str] = Field(default_factory=list)
    status: str = Field(default="draft")

    class Settings:
        name = "articles"
        indexes = ["author_email", "status", "created_at"]
```

```python
# src/app/tune.py - Register model
from vibetuner import VibetunerApp
from app.models import Article
from app.frontend.routes import post_routes

app = VibetunerApp(
    models=[Article],  # Registers model with database
    routes=[post_routes],
)

# Framework automatically:
# ✅ Creates MongoDB collection if it doesn't exist
# ✅ Creates indexes for performance
# ✅ Validates all fields on insert/update
# ✅ Provides query operators
```

### Pattern 3: Template Hooks & Filters

Generate reusable response formatting:

```python
# src/app/frontend/templates.py
from datetime import datetime
from markupsafe import Markup

def format_timestamp(dt: datetime, format: str = "%Y-%m-%d %H:%M") -> str:
    """Format datetime for display."""
    return dt.strftime(format) if dt else ""

def badge(text: str, color: str = "blue") -> Markup:
    """Generate a styled badge element."""
    return Markup(
        f'<span class="badge badge-{color}">{text}</span>'
    )

def truncate(text: str, length: int = 50) -> str:
    """Truncate text to length with ellipsis."""
    return text[:length] + "..." if len(text) > length else text
```

```python
# src/app/tune.py - Register filters
from vibetuner import VibetunerApp
from app.frontend.templates import format_timestamp, badge, truncate

app = VibetunerApp(
    template_filters={
        "timestamp": format_timestamp,
        "badge": badge,
        "truncate": truncate,
    },
)
```

Usage in templates:

```jinja
<div>
  Created: {{ post.created_at | timestamp }}
  Status: {{ post.status | badge("green") }}
  Preview: {{ post.content | truncate(100) }}
</div>
```

### Pattern 4: Service Factory Pattern

Generate common service patterns:

```python
# src/app/services/base.py
from typing import Generic, TypeVar
from beanie import Document

T = TypeVar("T", bound=Document)

class BaseService(Generic[T]):
    """Base service with common CRUD operations."""

    def __init__(self, model: type[T]):
        self.model = model

    async def get_by_id(self, id: str) -> T | None:
        return await self.model.get(id)

    async def list(self, skip: int = 0, limit: int = 10) -> list[T]:
        return await self.model.find().skip(skip).limit(limit).to_list(limit)

    async def create(self, data: dict) -> T:
        instance = self.model(**data)
        await instance.insert()
        return instance

    async def update(self, id: str, data: dict) -> T | None:
        instance = await self.get_by_id(id)
        if instance:
            await instance.update({"$set": data})
        return instance

    async def delete(self, id: str) -> bool:
        result = await self.model.delete_one({"_id": id})
        return result.deleted_count > 0

# Use it:
class PostService(BaseService[Post]):
    """Service for Post CRUD."""
    pass

post_service = PostService(Post)
```

### Pattern 5: Validation Schema Generator

```python
# src/app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from app.models import User, Post

# Generate schema from model
class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        from_attributes = True

class PostCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=10)
    tags: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True

class PostUpdateSchema(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None

    class Config:
        from_attributes = True
```

Routes use these:

```python
@router.post("/api/posts", status_code=201)
async def create_post(data: PostCreateSchema, request: Request):
    """Create new post."""
    # Validation automatic via Pydantic
    post = await Post.create(**data.model_dump())
    return PostSchema.from_orm(post)
```

---

### Code Generation Workflow

**Before Work:**

1. Define requirements clearly
2. Sketch out data models
3. Plan API endpoints

**During Work:**

1. Write models first (data-driven)

   ```bash
   touch src/app/models/feature.py
   ```

2. Generate CRUD endpoints

   ```python
   from vibetuner.crud import create_crud_routes
   routes = create_crud_routes(MyModel, ...)
   ```

3. Add tests for custom logic (non-generated)
4. Generate templates if needed

**After Work:**

1. Run full test suite
2. Verify generated code matches requirements
3. Add custom business logic on top

---

## Part 3: TDD + Code Generation Combined

### Workflow: Generate → Test → Refine

```bash
# Step 1: Define model
# (Create src/app/models/item.py with validation)

# Step 2: Generate routes
# (Use create_crud_routes)

# Step 3: Run generated tests
uv run pytest tests/test_item_routes.py -v

# Step 4: Add custom logic
# (Modify routes to add business rules)

# Step 5: Add tests for custom logic
# (Write service tests for business logic)

# Step 6: Verify everything
just type-check
jest lint
uv run pytest -v
```

### Example: Generate & Extend

**Generate base CRUD:**

```python
# Auto-generated routes (from CRUD factory)
from vibetuner.crud import create_crud_routes
from app.models import Article

article_routes = create_crud_routes(
    Article,
    prefix="/api/articles",
    tags=["articles"],
)
# Provides: GET/POST/GET/{id}/PATCH/{id}/DELETE/{id}
```

**Extend with custom logic:**

```python
# src/app/frontend/routes/articles.py
from fastapi import APIRouter, Depends, HTTPException
from app.models import Article
from app.services.article import publish_article, notify_subscribers

router = APIRouter()

# Include auto-generated routes
router.include_router(article_routes)

# Add custom endpoint
@router.post("/api/articles/{id}/publish")
async def publish_article_endpoint(
    id: str,
    request: Request,
    user = Depends(get_current_user)
):
    """Publish an article and notify subscribers."""
    article = await Article.get(id)
    if not article:
        raise HTTPException(status_code=404)

    if article.author_id != user.id:
        raise HTTPException(status_code=403)

    # Custom business logic
    published = await publish_article(article)
    await notify_subscribers(published)

    return {"status": "published", "published_at": published.published_at}
```

**Test the custom logic:**

```python
# tests/test_article_publish.py
@pytest.mark.asyncio
async def test_publish_article_notifies_subscribers():
    """Publishing sends notifications to subscribers."""
    article = await Article.create(title="Test", content="...")

    with patch("app.services.article.notify_subscribers") as mock:
        response = await client.post(f"/api/articles/{article.id}/publish")
        assert response.status_code == 200
        mock.assert_called_once()
```

---

## Checklist: TDD Development Cycle

```markdown
## [ ] RED Phase

- [ ] Write failing test first
- [ ] Describe expected behavior clearly
- [ ] Test covers one scenario only
- [ ] Confirm test fails: `uv run pytest -v`

## [ ] GREEN Phase  

- [ ] Write minimal code to pass test
- [ ] Don't add extra features yet
- [ ] Run test - confirm it passes
- [ ] All other tests still pass

## [ ] REFACTOR Phase

- [ ] Improve code quality
- [ ] Ensure test still passes
- [ ] Run full suite: `uv run pytest -v`
- [ ] Format & lint: `just format && just lint`

## [ ] Code Generation

- [ ] Use CRUD factory for endpoints
- [ ] Generate schemas from models
- [ ] Let framework handle validation
- [ ] Test custom logic only

## [ ] Ready to Commit

- [ ] All tests passing
- [ ] Code formatted
- [ ] Type checking passes
- [ ] Docstrings added
- [ ] Atomic commit message
```

---

## Resources

- **Testing with pytest**: https://docs.pytest.org/
- **Beanie (MongoDB ODM)**: https://beanie-odm.readthedocs.io/
- **FastAPI Testing**: https://fastapi.tiangolo.com/advanced/testing-dependencies/
- **Vibetuner CRUD**: https://vibetuner.alltuner.com/llms.txt (search "CRUD")
- **vibetuner Repository**: https://github.com/alltuner/vibetuner
