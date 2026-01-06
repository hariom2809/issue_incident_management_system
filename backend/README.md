env configuration:
    python: 3.10
    postgress: 18

setup:
    1. Make virtual environment
        cd backend
        py -3.10 -m venv venv

    2. Activate virtual environment
        venv\Scripts\Activate

    3. Install the requirements
        pip install -r requirements.txt
        
    4. Run the application
        python -m uvicorn app.main:app --reload