from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from datetime import date
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.user_exam import UserExam
from app.schemas.user_exam import UserExamCreate

def get_all_exams(db: Session) -> List[Exam]:
    return db.query(Exam).all()

def get_exam_with_syllabus(db: Session, exam_id: int) -> Optional[Exam]:
    return (
        db.query(Exam)
        .options(joinedload(Exam.subjects).joinedload(Subject.topics))
        .filter(Exam.id == exam_id)
        .first()
    )

def calculate_total_syllabus_hours(exam: Exam) -> float:
    return sum(
        topic.estimated_hours
        for subject in exam.subjects
        for topic in subject.topics
    )

def create_user_exam(db: Session, user_id: int, data: UserExamCreate) -> UserExam:
    # Check if user already has an exam enrollment
    existing = db.query(UserExam).filter(UserExam.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already enrolled in an exam")

    # Verify exam exists
    exam = db.query(Exam).filter(Exam.id == data.exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    user_exam = UserExam(
        user_id=user_id,
        exam_id=data.exam_id,
        exam_date=data.exam_date,
        study_hours_per_day=data.study_hours_per_day,
    )
    db.add(user_exam)
    db.commit()
    db.refresh(user_exam)
    return user_exam

def build_user_exam_response(db: Session, user_exam: UserExam) -> dict:
    exam = get_exam_with_syllabus(db, user_exam.exam_id)
    total_hours = calculate_total_syllabus_hours(exam)
    days_remaining = (user_exam.exam_date - date.today()).days
    required_per_day = round(total_hours / days_remaining, 2) if days_remaining > 0 else 0.0
    return {
        "id": user_exam.id,
        "exam_id": user_exam.exam_id,
        "exam_date": user_exam.exam_date,
        "study_hours_per_day": user_exam.study_hours_per_day,
        "created_at": user_exam.created_at,
        "days_remaining": days_remaining,
        "total_syllabus_hours": total_hours,
        "required_hours_per_day": required_per_day,
    }
