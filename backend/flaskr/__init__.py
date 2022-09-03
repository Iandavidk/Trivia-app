import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        all_categories = [category.format() for category in categories]
    
    if len(all_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': all_categories,
      'total_categories': len(all_categories)
    })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/questions')
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            "categories": [category.format() for category in categories],
            'current_category': None
        })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter(Question.id==question_id).one_or_none()
    
        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
    
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        if question is None or answer is None or category is None or difficulty is None:
            abort(400)

        try:
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
        
            new_question.insert()

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': current_questions,
                'total_questions': len(questions)
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()

        if body is None or body['search_term'] is None:
            abort(400)

        search_term = body.get('search_term')
        results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        if len(results) == 0:
            abort(404)

        matching_questions = paginate_questions(request, results)

        return jsonify({
            'success': True,
            'questions': matching_questions,
            'total_results': len(results)
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def questions_by_categories(category_id):

        category = Category.query.get(category_id)

        if category is None:
            abort(404)

        category_questions = Question.query.filter(Question.category==category_id).all()
        questions = paginate_questions(request, category_questions)

        if len(questions) == 0:
            abort(404)

        return jsonify({
        'success': True,
        'questions': questions,
        'total_results': len(category_questions),
        'current_category': category.id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quiz', methods=['POST'])
    def quiz_questions():
        body = request.get_json()

        if body is None or body['previous_questions'] is None or body['category'] is None:
            abort(400)

        try:
            previous_questions = body.get('previous_questions')
            category = body.get('category')

            if category == 0:
                questions = Question.query.order_by(func.random())
            else:
                questions = Question.query.filter(Question.category==category).order_by(func.random())

            question = questions.filter(Question.id.notin_(previous_questions)).first()

            if question is None:
                return jsonify({
                'success': True
                })

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

