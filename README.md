For database setup:
    1. Download the Postgress 18 ;
        make a new database by the name "issue_incident_db" ;
    2. Change the connection string inside the .env file inside the backend/app folder ;
    3. Run the db update command ;
        "alembic upgrade head" ;
    4. Run seed file once to hae the RBAC correctly working ;
        "cd backend" ;
        "py -m app.database.seed_rbac" ;

    
