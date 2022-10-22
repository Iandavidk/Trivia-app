# API Development and Documentation Final Project

## Trivia App

This app is a full-stack trivia game where users can test their knowledge answering trivia questions. The app has been built using TDD principles:

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

## Backend

The [backend](https://github.com/Iandavidk/Trivia-app/tree/main/backend) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

See the [Backend README.md](https://github.com/Iandavidk/Trivia-app/blob/main/README.md) for more information

## Frontend

The [frontend](https://github.com/Iandavidk/Trivia-app/tree/main/frontend) app was built using create-react-app and uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository.

The frontend should be fairly straightforward and digestible. While working on your backend request handling and response formatting, you can reference the frontend to view how it parses the responses. You are not required to make any edits, but if choose to do so, you'll primarily work within the [components](https://github.com/Iandavidk/Trivia-app/tree/main/frontend/src/components) folder where you'll find the endpoints utilized by the components.

After you complete your endpoints, ensure you return to the frontend to confirm your API handles requests and responses appropriately:

- Endpoints defined as expected by the frontend
- Response body provided as expected by the frontend




