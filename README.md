# Exam Plan Tracker

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd exam-plan-tracker
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API:**
   - Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
   - Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
