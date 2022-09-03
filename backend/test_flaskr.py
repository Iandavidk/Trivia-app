import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:Autodesk123!@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'What is the name of this app?',
            'answer': 'Trivia',
            'category': 5,
            'difficulty': 1
        }

        self.new_question_missing = {
            'question': 'What is the name of this app?',
            'category': 5,
            'difficulty': 1
        }

        self.new_question_invalid = {
            'question': 'What is the name of this app?',
            'answer': 'Trivia',
            'category': 5,
            'difficulty': "invalid difficulty"
        }

        self.quiz = {
            'previous_questions': [6, 11, 19, 21],
            'category': 0
        }

        self.quiz_completed = {
            'previous_questions': [16, 17, 18],
            'category': 2
        }

        self.quiz_invalid = {
            'previous_questions': 16,
            'category': 2
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Getting all categories
    def test_categories_retrieval(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    # Getting all questions
    def test_questions_retrieval(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    def test_404_no_questions_found(self):
        res = self.client().get('/questions?page=0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_questions_beyond_existing(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Deleting a question
    def test_question_deletion(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id==10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)
        self.assertEqual(data['deleted'], 10)
        self.assertTrue(data['success'])

    def test_404_non_exisiting_question_deletion(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Creating a question
    def test_question_creation(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_400_question_creation_data_missing(self):
        res = self.client().post('/questions', json=self.new_question_missing)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_question_creation_invalid_data(self):
        res = self.client().post('/questions', json=self.new_question_invalid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Searching for questions
    def test_questions_search(self):
        res = self.client().post('/questions/search', json={'search_term': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_results'])
        self.assertTrue(len(data['questions']))

    def test_400_no_search_term(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_404_no_questions_found(self):
        res = self.client().post('/questions/search', json={'search_term': 'bestbuddy'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Getting questions by category
    def test_questions_retrieval_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_results'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], 1)

    def test_404_category_does_not_exist(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_no_questions_in_this_category(self):
        res = self.client().get('/categories/1/questions?page=0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Playing the quiz
    def test_random_quiz(self):
        res = self.client().post('/quiz', json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_400_quiz_missing_data(self):
        res = self.client().post('/quiz')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_quiz_invalid_data(self):
        res = self.client().post('/quiz', json=self.quiz_invalid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_random_quiz_completed(self):
        res = self.client().post('/quiz', json=self.quiz_completed)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()