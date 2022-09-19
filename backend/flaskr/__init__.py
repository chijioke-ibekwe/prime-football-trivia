from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Option

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

    return app