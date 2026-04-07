import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # Always use the same connection for in-memory SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)

# Tests for Task API endpoints

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_task():
    response = client.post("/tasks/", json={"title": "Learn Docker"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Learn Docker"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_with_description():
    response = client.post("/tasks/", json={
        "title": "Learn Terraform",
        "description": "Learn Terraform documentation"
    })
    assert response.status_code == 201
    assert response.json()["description"] == "Learn Terraform documentation"


def test_create_task_empty_title():
    """An empty title should trigger a validation error."""
    response = client.post("/tasks/", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks():
    client.post("/tasks/", json={"title": "Task A"})
    client.post("/tasks/", json={"title": "Task B"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task():
    created = client.post("/tasks/", json={"title": "My task"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "My task"


def test_get_task_not_found():
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task():
    created = client.post("/tasks/", json={"title": "Old title"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={
        "title": "New title",
        "completed": True
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["completed"] is True


def test_update_task_partial():
    """PATCH partiel — seul completed change, title reste intact."""
    created = client.post("/tasks/", json={"title": "Old title"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Old title"
    assert response.json()["completed"] is True


def test_delete_task():
    created = client.post("/tasks/", json={"title": "To delete"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 404


def test_delete_task_not_found():
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
