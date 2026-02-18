For database setup:
    Download the Postgress 18 
    Change the connection string inside the .env file inside the backend/app folder
    Run the db update command 
        "alembic upgrade head"
    Run seed file once to hae the RBAC correctly working 
        "cd backend"
        "py -m app.database.seed_rbac"

    