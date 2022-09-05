# API Development and Documentation Final Project

## Trivia App

This app is a full-stack trivia game where users can test their knowledge answering trivia questions. The app has been bult using TDD principles:

The application has the following functionality:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Overview

### Tech Stack

Tech stack includes:

- React.js for the applications's frontend.
- Python3 and Flask as the server-side language and server-side framework respectively.
- PostgreSQL is the database used in the application.
- SQLAlchemy ORM is the Object Relational Mapping(ORM) library.

## Getting Started

### Database Configuration

Make sure to have PostgreSQL installed, if it is not, execute:

```bash
sudo apt-get -y install postgresql
```

#### Create Database

First, start your PostgreSQL database server by running:

```bash
sudo service postgresql start
```

Then, create your project's database by running:

```bash
createdb trivia
```

#### Database Connection String

Add your database connection string as an environment variable by executing:

```bash
export DATABASE_URL=<db_connection_string> # e.g. postgresql://username:password@localhost:5432/database
```

#### Import Database

Make sure to be inside the `/backend` directory. To import the database schema and initial data, run:

```bash
psql trivia < trivia.psql
```

### Installation and Running the Servers

#### Backend

Navigate to the `/backend` directory and make sure that you have **Python3** installed.

##### Create Virtual Environment

Run the following to create a virtual environment:

```bash
python3 -m virtualenv env
```

Activate your newly created virtual environment by running:

```bash
source env/bin/activate
```

##### Installing Backend Dependencies

To install backend dependencies, simply run:

```bash
pip install -r requirements.txt
```

##### Running the Backend Server

Prepare the development environment by executing:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
```

To run the server at any time, use:

```bash
flask run
```

By default, the Flask server runs on [http://localhost:5000](http://localhost:5000).

#### Frontend Dependencies

Navigate to the `/frontend` directory and make sure that you have **Node.js** and **npm** installed first.

##### Installing Frontend Dependencies

To install backend dependencies, simply run:

```bash
npm install
```

##### Running the Frontend Server

To start the frontend server, run:

```bash
npm start
```

This will run the React frontend server at [http://localhost:3000](http://localhost:3000).

## Testing

To run the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

_Omit the `dropdb` command the first time you run tests._

## API Reference

- Base URL:

  - currently this application is only hosted locally.
  - The backend is hosted at `http://127.0.0.1:5000/`.

- Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:

```json
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

The API returns three types of errors:

- 404: resource not found.
- 400: bad request.
- 422: unprocessable.

### Endpoints

#### GET /categories

- General: 
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": [
    {
      "1": "Science"
    },
    {
      "2": "Art"
    },
    {
      "3": "Geography"
    },
    {
      "4": "History"
    },
    {
      "5": "Entertainment"
    },
    {
      "6": "Sports"
    }
  ],
  "success": true,
  "total_categories": 6
}
```

#### GET /questions

- General:

  - Returns a list questions.
  - Results are paginated in groups of 10.
  - Also returns a list of categories and the total number of questions.

- Sample: `curl http://127.0.0.1:5000/questions`

```json
{
  "categories": [
    {
      "1": "Science"
    },
    {
      "2": "Art"
    },
    {
      "3": "Geography"
    },
    {
      "4": "History"
    },
    {
      "5": "Entertainment"
    },
    {
      "6": "Sports"
    }
  ],
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### DELETE /questions/\<int:id\>

- General:
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

- Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`

```json
{
  "deleted": 6,
  "success": true
}
```

#### POST /questions

- General:

  - Creates a new question using JSON request parameters.
  - Returns JSON object with the newly created question id, as well as paginated questions.
  - Also returns the updated number of total questions.

- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Which US state contains an area known as the Upper Penninsula?", "answer": "Michigan", "difficulty": 3, "category": "3"}'`

```json
{
  "created": 26,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### POST /questions/search

- General:

  - Searches for questions using search term in JSON request parameters.
  - Returns JSON object with paginated matching questions.
  - Also returns total number of matching questions.

- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"search_term": "title"}'`

```json
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_results": 2
}
```

#### GET /categories/\<int:category_id>\/questions

- General:

  - Gets questions by category id, using url parameters.
  - Returns JSON object with paginated matching questions.
  - Also returns total number of the category's questions.

- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```json
{
  "current_category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "success": true,
  "total_results": 3
}
```

#### POST /quiz

- General:

  - Allows users to play a quiz game.
  - Uses JSON request parameters of category and previous questions.
  - Returns JSON object with a random question that is not among previous questions.

- Sample: `curl http://127.0.0.1:5000/quiz -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "category": 1}'`

```json
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```
