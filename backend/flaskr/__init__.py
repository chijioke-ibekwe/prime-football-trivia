from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Option

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]

    return current_questions

def create_app(test_config=None):
    app = Flask(__name__)
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

    @app.route('/questions', methods=['POST'])
    def create_question():
        payload = request.get_json()
        try:
            question = Question(question=payload.get('question'), answer=payload.get('answer'), difficulty=int(payload.get('difficulty'))) 
            option_data = payload.get('options')
            id = question.insert()

            for key, value in option_data.items():
                option = Option(option=value, letter=key, question_id=id)
                option.insert()
            
            questions = Question.query.all()

            return jsonify({
                'totalQuestions': len(questions),
            })
        except:
            abort(422)

    @app.route('/questions', methods=['GET'])
    def get_all_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'questions': current_questions,
            'totalQuestions': len(questions)
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)
        
        question.delete()

        return jsonify({
            'status': 'Successful',
            'message': 'Question deleted successfully'
        })

    return app