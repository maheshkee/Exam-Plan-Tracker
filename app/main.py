from fastapi import FastAPI

app = FastAPI(title="exam-plan-tracker")

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "exam-plan-tracker"}
