# Prime Football Trivia
RESTful APIs for a trivia game to test your football knowledge. As a lover of football and having played a number of trivia games online that weren't challenging enough, I was inspired to work on this project. If you think you know football, play the Prime Football Trivia 😌. Frontend component of the application to be integrated soon.

## Getting Started

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `prime-football-trivia` database:

```bash
createbd prime-football-trivia
```

Populate the database using the `prime-football-trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql prime-football-trivia < prime-football-trivia.psql
```

### Run the Server

From within the `/backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

This application contains the following endpoints:

1. `POST '/api/v1/questions'`

- Creates a question on the application.
- Body: An object containing the details of the question and the options as shown below:

```json
{
    "question": "With 260 goals, who is the Premier League's all-time top scorer?",
    "answer": "A",
    "difficulty": 3,
    "options": {
        "A": "Alan Shearer",
        "B": "Thierry Henry",
        "C": "Didier Drogba",
        "D": "Sergio Aguero"
    }
}
```
- Returns: An object containing the id of the question created and the total questions available on the app.

```json
{
    "status": "Successful",
    "message": "Question created successfully",
    "data": {
        "id": 10,
        "totalQuestions": 6
    }
}
```

2. `GET '/api/v1/questions?page=${integer}'`

- Fetches a list of objects containing the details of each question available on the app.
- Request Arguments: 'page' query parameter (integer)

```json
{
    "status": "Successful",
    "message": null,
    "data": [
        {
            "id": 1,
            "question": "Who was the only player to miss in the 2006 World Cup finals penalty shoot-out?",
            "options": {
                "A": "Claude Makelele",
                "B": "Patrick Vieira",
                "C": "Florent Malouda",
                "D": "David Trezeguet"
            },
            "answer": "D",
            "difficulty": 4
        },
                .
                .
                .
    ],
    "page": {
        "size": 10,
        "totalElements": 100,
        "totalPages": 1,
        "number": 1
    }
}
```

3. `GET '/api/v1/questions/<int:question_id>'`

- Fetches a single question on the app by ID.

```json
{
    "status": "Successful",
    "message": null,
    "data": [
        {
            "id": 1,
            "question": "Who was the only player to miss in the 2006 World Cup finals penalty shoot-out?",
            "options": {
                "A": "Claude Makelele",
                "B": "Patrick Vieira",
                "C": "Florent Malouda",
                "D": "David Trezeguet"
            },
            "answer": "D",
            "difficulty": 4
        }
    ],
    "page": {
        "size": 10,
        "totalElements": 1,
        "totalPages": 1,
        "number": 1
    }
}
```

4. `PATCH '/api/v1/questions/<int:question_id>'`

- Updates a question on the application by ID.
- Body: An object containing the details of question properties you want to update as shown below (no property is required):

```json
{
    "question": "With 260 goals, who is the Premier League's all-time top scorer?",
    "answer": "A",
    "difficulty": 3,
    "options": {
        "A": "Alan Shearer",
        "B": "Thierry Henry",
        "C": "Didier Drogba",
        "D": "Sergio Aguero"
    }
}
```
- Returns: An object containing the id of the question updated and the total questions available on the app.

```json
{
    "status": "Successful",
    "message": "Question updated successfully",
    "data": {
        "id": 10,
        "totalQuestions": 6
    }
}
```

5. `DELETE '/api/v1/questions/${question_id}'`

- Deletes a question on the application by ID.
- Returns: An object containing the status of the request as shown below:

```json
{
    "status": "Successful",
    "message": "Question deleted successfully",
    "data": null
}
```

6. `POST '/api/v1/trivia'`

- Simulates a game and returns a random question with the associated options from the app which has not been previously returned.
- Body: An object containing the level of question dfficulty (EASY, NORMAL or HARD) you require and list of the questions that have been asked.

```json
{
    "difficulty": "NORMAL",
    "previousQuestions": [12, 24, 36]
}
```

- Returns: An object containing a single question with the associated options as shown:

```json
{
    "status": "Successful",
    "message": null,
    "data": [
        {
            "id": 1,
            "question": "Who was the only player to miss in the 2006 World Cup finals penalty shoot-out?",
            "options": {
                "A": "Claude Makelele",
                "B": "Patrick Vieira",
                "C": "Florent Malouda",
                "D": "David Trezeguet"
            },
            "answer": "D",
            "difficulty": 4
        }
    ]
}
```

## Author

- Chijioke Ibekwe (https://github.com/chijioke-ibekwe)
