import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["ENABLE_SCHEDULER"] = "False"

from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    import app.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(setup_database):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    client.close()
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def seeded_db(setup_database):
    from app.models import Exam, Subject, Topic
    db = TestingSessionLocal()
    try:
        if db.query(Exam).count() == 0:
            exam = Exam(name="GATE CS", description="Test exam")
            exam2 = Exam(name="SSC CGL", description="Second test exam")
            db.add_all([exam, exam2])
            db.flush()

            subject = Subject(exam_id=exam.id, name="Operating Systems")
            subject2 = Subject(exam_id=exam2.id, name="Quantitative Aptitude")
            db.add(subject)
            db.add(subject2)
            db.flush()

            topics = [
                Topic(subject_id=subject.id, name="Process Management", estimated_hours=7.0),
                Topic(subject_id=subject.id, name="CPU Scheduling", estimated_hours=5.0),
                Topic(subject_id=subject2.id, name="Number System", estimated_hours=4.0),
            ]
            db.add_all(topics)
            db.commit()
    finally:
        db.close()

@pytest.fixture(scope="session")
def auth_headers(client, seeded_db):
    client.post("/auth/register", json={"email": "testuser@test.com", "password": "testpass123"})
    res = client.post("/auth/login", json={"email": "testuser@test.com", "password": "testpass123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
