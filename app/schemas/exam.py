from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class TopicResponse(BaseModel):
    id: int
    name: str
    estimated_hours: float
    model_config = ConfigDict(from_attributes=True)

class SubjectResponse(BaseModel):
    id: int
    name: str
    topics: List[TopicResponse] = []
    model_config = ConfigDict(from_attributes=True)

class ExamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ExamDetailResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    subjects: List[SubjectResponse] = []
    model_config = ConfigDict(from_attributes=True)
