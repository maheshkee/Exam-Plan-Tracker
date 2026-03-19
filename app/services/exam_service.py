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

def get_active_enrollment(db: Session, user_id: int) -> UserExam:
    """Get currently active enrollment or raise 404."""
    enrollment = (
        db.query(UserExam)
        .filter(
            UserExam.user_id == user_id,
            UserExam.is_active.is_(True),
        )
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="No active enrollment")
    return enrollment

def get_all_enrollments(db: Session, user_id: int) -> List[UserExam]:
    """Get all enrollments for a user."""
    return (
        db.query(UserExam)
        .filter(UserExam.user_id == user_id)
        .order_by(UserExam.created_at.desc(), UserExam.id.desc())
        .all()
    )

def switch_active_exam(db: Session, user_id: int, user_exam_id: int) -> UserExam:
    """Switch active exam to a different enrollment."""
    target = (
        db.query(UserExam)
        .filter(
            UserExam.id == user_exam_id,
            UserExam.user_id == user_id,
        )
        .first()
    )
    if not target:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.query(UserExam).filter(UserExam.user_id == user_id).update({"is_active": False})
    target.is_active = True
    db.commit()
    db.refresh(target)
    return target

def create_user_exam(db: Session, user_id: int, data: UserExamCreate) -> UserExam:
    # Check if user already has an enrollment for this exam
    existing = (
        db.query(UserExam)
        .filter(
            UserExam.user_id == user_id,
            UserExam.exam_id == data.exam_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this exam")

    # Deactivate all current enrollments
    db.query(UserExam).filter(UserExam.user_id == user_id).update({"is_active": False})

    # Verify exam exists
    exam = db.query(Exam).filter(Exam.id == data.exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    user_exam = UserExam(
        user_id=user_id,
        exam_id=data.exam_id,
        exam_date=data.exam_date,
        study_hours_per_day=data.study_hours_per_day,
        is_active=True,
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
        "is_active": user_exam.is_active,
        "created_at": user_exam.created_at,
        "days_remaining": days_remaining,
        "total_syllabus_hours": total_hours,
        "required_hours_per_day": required_per_day,
    }
