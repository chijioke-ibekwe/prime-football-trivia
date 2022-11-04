import math
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Option

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = []

    for question in selection:
        formatted_options = {}
        for option in question.options:
            formatted_options[option.letter] = option.option
        formatted_questions.append(question.format(formatted_options))

    current_questions = formatted_questions[start:end]

    return current_questions


def to_response_object(data, total_size, request, message):
    page = {'size': QUESTIONS_PER_PAGE,
    'totalElements': total_size,
    'totalPages': math.ceil(total_size/QUESTIONS_PER_PAGE),
    'number': request.args.get('page', 1, type=int)}

    if request.method == 'GET':
        return jsonify({
            'status': 'Successful',
            'message': message,
            'data': data,
            'page': page
        })
    else: 
        return jsonify({
            'status': 'Successful',
            'message': message,
            'data': data
        })


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE,OPTIONS"
        )
        return response


    @app.route('/api/v1/questions', methods=['POST'])
    def create_question():
        payload = request.get_json()
        option_data = payload.get('options')

        if len(option_data.items()) != 4:
            abort(400, 'Number of options provided must be 4')
        try:
            question = Question(question=payload.get('question'), answer=payload.get('answer'), difficulty=int(payload.get('difficulty'))) 

            id = question.insert()

            for key, value in option_data.items():
                option = Option(option=value, letter=key, question_id=id)
                option.insert()
            
            questions = Question.query.all()
            totalQuestions = {}
            totalQuestions['id'] = id
            totalQuestions['totalQuestions'] = len(questions)

            return to_response_object(totalQuestions, 0, request, 'Question created successfully')
        except:
            abort(422)


    @app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
    def get_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404, 'Question not found')

        questions = []
        questions.append(question)

        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404, 'Question not found')

        return to_response_object(current_questions, len(questions), request, None)


    @app.route('/api/v1/questions', methods=['GET'])
    def get_all_questions():
        questions = Question.query.order_by(Question.id).all()

        current_questions = paginate_questions(request, questions)

        return to_response_object(current_questions, len(questions), request, None)


    @app.route('/api/v1/questions/<int:question_id>', methods=['PATCH'])
    def update_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        option_data = {}

        if question is None:
            abort(404, 'Question not found')
            
        payload = request.get_json()
        try:
            if payload.get('question'):
                question.question = payload.get('question')

            if payload.get('answer'):
                question.answer = payload.get('answer')

            if payload.get('difficulty'):
                question.difficulty = int(payload.get('difficulty'))

            id = question.update()

            if payload.get('options'): 
                option_data = payload.get('options')

                for key, value in option_data.items():
                    option = Option.query.filter(Option.question_id == question_id, Option.letter == key).one_or_none()

                    if option:
                        option.option = value
                        option.update()
            
            questions = Question.query.all()
            totalQuestions = {}
            totalQuestions['id'] = id
            totalQuestions['totalQuestions'] = len(questions)

            return to_response_object(totalQuestions, 0, request, 'Question updated successfully')
        except:
            abort(422, 'An error occurred while processing update')


    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404, 'Question not found')
        
        question.delete()

        return to_response_object(None, 0, request, 'Question deleted successfully')

    
    @app.route('/api/v1/trivia', methods=['POST'])
    def get_trivia_question():
        payload = request.get_json()
        difficulty = payload.get('difficulty')
        previous_questions = payload.get('previousQuestions')

        if difficulty == 'EASY':
            difficulty_level = [1, 2]
        elif difficulty == 'NORMAL':
            difficulty_level = [3, 4]
        elif difficulty == 'HARD':
            difficulty_level = [5]
        else:
            difficulty_level = [1, 2, 3, 4, 5]

        questions = Question.query.filter(Question.difficulty.in_(difficulty_level), ~Question.id.in_(previous_questions)).order_by(Question.id).all()
        
        length = len(questions)
        questions_array = []
        if length == 0:
            return to_response_object(questions_array, len(questions_array), request, None)

        random_question = questions[random.randrange(length)]
        questions_array.append(random_question)

        current_question = paginate_questions(request, questions_array)

        return to_response_object(current_question, length, request, None)


    @app.errorhandler(400)
    def client_error(error):
        return jsonify({
            'status': 'Failed',
            'message': error.description,
            'data': None
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'Failed',
            'message': error.description,
            'data': None
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'status': 'Failed',
            'message': error.description,
            'data': None
        }), 422

    return app