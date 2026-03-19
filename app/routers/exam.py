from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.exam import ExamResponse, ExamDetailResponse
from app.schemas.user_exam import UserExamCreate, UserExamResponse
from app.utils.dependencies import get_current_user
from app.services import exam_service

router = APIRouter(prefix="/exams", tags=["exams"])

@router.post("/enroll", response_model=UserExamResponse, status_code=status.HTTP_201_CREATED)
def enroll_exam(
    data: UserExamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_exam = exam_service.create_user_exam(db, current_user.id, data)
    return exam_service.build_user_exam_response(db, user_exam)

@router.get("/my-enrollment", response_model=UserExamResponse)
def get_my_enrollment(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_exam = exam_service.get_active_enrollment(db, current_user.id)
    return exam_service.build_user_exam_response(db, user_exam)

@router.get("/my-enrollments", response_model=List[UserExamResponse])
def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enrollments = exam_service.get_all_enrollments(db, current_user.id)
    return [exam_service.build_user_exam_response(db, enrollment) for enrollment in enrollments]

@router.post("/switch/{user_exam_id}", response_model=UserExamResponse)
def switch_exam(
    user_exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_exam = exam_service.switch_active_exam(db, current_user.id, user_exam_id)
    return exam_service.build_user_exam_response(db, user_exam)

@router.get("", response_model=List[ExamResponse])
def list_exams(db: Session = Depends(get_db)):
    return exam_service.get_all_exams(db)

@router.get("/{exam_id}", response_model=ExamDetailResponse)
def get_exam_detail(exam_id: int, db: Session = Depends(get_db)):
    exam = exam_service.get_exam_with_syllabus(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam
