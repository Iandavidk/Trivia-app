import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
from sqlalchemy import func

from models import setup_db, Question, Category

# To be used in paginating the questions
QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
        #sets a default value for the "page" variable, which is 1 unless otherwise specified.
        page = request.args.get('page', 1, type=int)
        #sets a default value for the "start" variable
        start =  (page - 1) * QUESTIONS_PER_PAGE
        #sets a default value for the "end" variable
        end = start + QUESTIONS_PER_PAGE
        #creates a list of questions from the selection
        questions = [question.format() for question in selection]
        #returns the questions from the list, starting at the "start" variable and ending at the "end" variable.
        return questions[start:end]

def create_app(test_config=None):
    """
    Create the app itself.
    @param test_config - the test config for the app itself.
    @returns the app itself
    """
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
    def get_all_categories():
        #defines a function that will return a JSON response with the category types for a given category id.
        categories = Category.query.all()
        categoriesDict = {}
        """
        The code iterates through all of the category objects in the Category.query.all() collection and stores the type for each category in a dictionary.
        """
        for category in categories:
            categoriesDict[category.id] = category.type 
        #returns the JSON response with the success flag set to True and the categories dictionary as the value.
        return jsonify({
            'success': True,
            'categories': categoriesDict
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

    @app.route('/questions')
    def retrieve_questions():
        #Retrieves all questions from the database.
        questions = Question.query.order_by(Question.id).all()
        #Retrieves all categories from the database
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        #Checks to see if there are any questions. If there are no questions, it sends back a 404 error.
        if len(current_questions) == 0:
            abort(404)
        """
        Returns a JSON object with the following information: 
        - "success" is set to True if everything went okay. 
        - "questions" is a list of all the questions in the database. 
        - "total_questions" is the total number of questions in the database. 
        - "categories" is a list of all the categories in the database. 
        - "current_category" is set to None if the user is not currently on a category page.
        """
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
        try:
            #filters the questions in the database to find the question with the given id.
            question = Question.query.filter(Question.id==question_id).one_or_none()
            #If the question is not found, the code aborts with a 404 error.
            if question is None:
                abort(404)
            #deletes the question from the database.
            question.delete()
            #returns a success message and the id of the deleted question.
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        
        except:
            abort(422)

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
        """
        The code starts by checking if the question, answer, category, and difficulty variables are set to None. 
        If they are, the code will abort and send back a 400 error.
        """
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        if question is None or answer is None or category is None or difficulty is None:
            abort(400)
        #If the question and answer variables are not set to None, the code will create a new Question object with the values of the question and answer variables.
        try:
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            #The code will then insert the new Question object into the questions list.
            new_question.insert()
            #The code will then get a list of all the questions in the database and paginate them using the paginate_questions function.
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)
            """
            The code will then send back a JSON response with the following information:

            - "success" will be set to True if the question was created successfully.
            - "created" will be set to the ID of the newly created question.
            - "questions" will be set to the list of questions that were paginated.
            - "total_questions" will be set to the total number of questions in the database.
            """
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
        """
        The code begins by checking if the body of the request is empty or if the 'searchTerm' key is empty.
        If either is true, the code aborts and sends a 400 HTTP status code.
        """
        try:
            if body is None or body['searchTerm'] is None:
                abort(400)
            #sets the 'searchTerm' key to the value of the 'body.get('searchTerm')' expression.
            searchTerm = body.get('searchTerm')
            #The code uses the 'Question.query.filter(Question.question.ilike(f'%{'searchTerm'}%')).all()' expression to get a list of all questions that match the search term.
            results = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
            #checks if the length of the list of questions is zero. If it is, the code aborts and sends a 404 HTTP status code.
            if len(results) == 0:
                abort(404)
            #paginate the list of questions.
            matching_questions = paginate_questions(request, results)
            """
            The code sets the 'success' key to True and the 'questions' key to the list of matching questions.
            The code sets the 'total_results' key to the length of the list of questions.
            """
            return jsonify({
                'success': True,
                'questions': matching_questions,
                'total_results': len(results)
            })

        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def questions_by_category(category_id):
        
        try:
            #The code tries to get a category by the given category_id.
            category =  Category.query.filter(Category.id == category_id).one_or_none()
            #If the category is not found, the code aborts and sends a 404 error.
            if category is None:
                abort(404)
            #The code gets all the questions in the given category and paginates them.
            category_questions = Question.query.filter(Question.category==category_id).all()
            questions = paginate_questions(request, category_questions)
            #If there are no questions in the category, the code sends a 404 error.
            if len(questions) == 0:
                abort(404)
            #The code returns the success, questions, and total_results variables.
            return jsonify({
            'success': True,
            'questions': questions,
            'total_results': len(category_questions),
            'current_category': category_id
            })

        except:
            abort(404)

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
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        #The code checks if the request is empty or if the previous questions and category are empty.
        if body is None or body['previous_questions'] is None or body['category'] is None:
            #If any of those are empty, the code aborts with a 400 HTTP status code
            abort(400)
        
        try:
            #Otherwise, the code retrieves the previous questions and category from the request body.
            previous_questions = body.get('previous_questions')
            category = body.get('category')
            
            if category == 0:
                #If the category is 0, the code randomly selects questions from the Question model to be used in the quiz.
                questions = Question.query.order_by(func.random())
            else:
                #Else, the code filters the questions by category and orders them randomly.
                questions = Question.query.filter(Question.category==category).order_by(func.random())
            #The code retrieves the first question from the filtered questions and formats it.
            question = questions.filter(Question.id.notin_(previous_questions)).first()
            #If the question is None, the code returns a success message.
            if question is None:
                return jsonify({
                'success': True
                })
            #Otherwise, the code returns the success message and the formatted question
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
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "request cannot be processed"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app

