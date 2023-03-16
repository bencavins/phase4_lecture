# phase4_lecture

### Set up db migrations

1. Create the migrations folder
    - `flask db init` (if the migrations folder already exists you can skip this)

2. Create db Models
    - update models.py
        - add columns to each class
        - define the relationships between classes
    - apply changes to database
        - create a new revision
            - `flask db revision --autogenerate -m 'your message here'`
        - check that the new revision file was created and has valid code
        - upgrade the database
            - `flask db upgrade head`
- **NOTE** this entire process needs to happen every time you update models

3. Populate database with seed data
    - look for a script called `seed.py`
        - run it if it exists
    - open the database and confirm data was added