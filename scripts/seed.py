import sys
from app.database import SessionLocal
from app.models import Exam, Subject, Topic

def get_or_create_exam(session, name):
    exam = session.query(Exam).filter_by(name=name).first()
    if not exam:
        print(f"Seeding {name}...")
        exam = Exam(name=name)
        session.add(exam)
        session.commit()
        session.refresh(exam)
    return exam

def get_or_create_subject(session, exam_id, name):
    subject = session.query(Subject).filter_by(exam_id=exam_id, name=name).first()
    if not subject:
        subject = Subject(exam_id=exam_id, name=name)
        session.add(subject)
        session.commit()
        session.refresh(subject)
    return subject

def get_or_create_topic(session, subject_id, name, hours):
    topic = session.query(Topic).filter_by(subject_id=subject_id, name=name).first()
    if not topic:
        topic = Topic(subject_id=subject_id, name=name, estimated_hours=hours)
        session.add(topic)
        session.commit()
        session.refresh(topic)
    return topic

def seed():
    session = SessionLocal()
    
    data = [
        {
            "exam": "GATE CS",
            "subjects": [
                {
                    "name": "Engineering Mathematics",
                    "topics": [
                        ("Linear Algebra", 8.0),
                        ("Calculus", 6.0),
                        ("Probability & Statistics", 7.0),
                        ("Discrete Mathematics", 9.0)
                    ]
                },
                {
                    "name": "Digital Logic",
                    "topics": [
                        ("Boolean Algebra", 5.0),
                        ("Combinational Circuits", 6.0),
                        ("Sequential Circuits", 7.0)
                    ]
                },
                {
                    "name": "Operating Systems",
                    "topics": [
                        ("Process Management", 7.0),
                        ("CPU Scheduling", 5.0),
                        ("Memory Management", 8.0),
                        ("File Systems", 5.0),
                        ("Deadlocks", 4.0)
                    ]
                },
                {
                    "name": "Computer Networks",
                    "topics": [
                        ("OSI & TCP/IP Model", 5.0),
                        ("Data Link Layer", 6.0),
                        ("Network Layer & Routing", 8.0),
                        ("Transport Layer", 5.0)
                    ]
                },
                {
                    "name": "Database Management Systems",
                    "topics": [
                        ("Relational Model & SQL", 8.0),
                        ("Normalization", 6.0),
                        ("Transactions & Concurrency", 7.0),
                        ("Indexing & Hashing", 5.0)
                    ]
                },
                {
                    "name": "Algorithms",
                    "topics": [
                        ("Sorting & Searching", 6.0),
                        ("Graph Algorithms", 9.0),
                        ("Dynamic Programming", 10.0),
                        ("Greedy Algorithms", 5.0)
                    ]
                }
            ]
        },
        {
            "exam": "SSC CGL",
            "subjects": [
                {
                    "name": "Quantitative Aptitude",
                    "topics": [
                        ("Number System", 5.0),
                        ("Percentages & Ratio", 4.0),
                        ("Algebra", 6.0),
                        ("Geometry & Mensuration", 7.0),
                        ("Time, Speed & Distance", 4.0)
                    ]
                },
                {
                    "name": "English Language",
                    "topics": [
                        ("Reading Comprehension", 5.0),
                        ("Grammar & Error Detection", 6.0),
                        ("Vocabulary", 4.0),
                        ("Sentence Rearrangement", 3.0)
                    ]
                },
                {
                    "name": "General Intelligence & Reasoning",
                    "topics": [
                        ("Analogy & Classification", 3.0),
                        ("Series & Patterns", 4.0),
                        ("Coding-Decoding", 3.0),
                        ("Logical Reasoning", 5.0)
                    ]
                },
                {
                    "name": "General Awareness",
                    "topics": [
                        ("History", 5.0),
                        ("Geography", 4.0),
                        ("Polity & Constitution", 5.0),
                        ("Current Affairs", 6.0),
                        ("Science & Technology", 4.0)
                    ]
                }
            ]
        },
        {
            "exam": "Banking (IBPS PO)",
            "subjects": [
                {
                    "name": "Quantitative Aptitude",
                    "topics": [
                        ("Data Interpretation", 8.0),
                        ("Number Series", 4.0),
                        ("Simplification & Approximation", 5.0),
                        ("Profit, Loss & Interest", 6.0)
                    ]
                },
                {
                    "name": "Reasoning Ability",
                    "topics": [
                        ("Puzzles & Seating Arrangement", 9.0),
                        ("Syllogisms", 4.0),
                        ("Blood Relations", 3.0),
                        ("Input-Output", 4.0)
                    ]
                },
                {
                    "name": "English Language",
                    "topics": [
                        ("Reading Comprehension", 6.0),
                        ("Cloze Test", 4.0),
                        ("Error Detection", 4.0)
                    ]
                },
                {
                    "name": "General Awareness (Banking)",
                    "topics": [
                        ("Banking & Financial Awareness", 7.0),
                        ("Current Affairs", 6.0),
                        ("Static GK", 5.0)
                    ]
                }
            ]
        }
    ]

    for exam_data in data:
        exam = get_or_create_exam(session, exam_data["exam"])
        for subject_data in exam_data["subjects"]:
            subject = get_or_create_subject(session, exam.id, subject_data["name"])
            for topic_name, hours in subject_data["topics"]:
                get_or_create_topic(session, subject.id, topic_name, hours)

    total_exams = session.query(Exam).count()
    total_subjects = session.query(Subject).count()
    total_topics = session.query(Topic).count()
    
    print("\n--- Final Summary ---")
    print(f"Total Exams: {total_exams}")
    print(f"Total Subjects: {total_subjects}")
    print(f"Total Topics: {total_topics}")
    
    session.close()

if __name__ == "__main__":
    seed()
