from flask import Flask, session
from flask_session import Session
from flask_cors import CORS
import redis
import os

app = Flask(__name__)
CORS(app)

# Configure Flask-Session for Redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))

Session(app)
questions = {	"0": {
        "initial": True,
        "text": "Welcome to MapDate. Are you ready to answer some questions to figure out exactly when your map was made?",
        "latlng": [
            54,
            15
        ],
        "questions": {
            "ok": "1"
        }
    },
    "1": {
        "initial": False,
        "text": "Istanbul or Constantinople?",
        "latlng": [41.0082, 28.9784],
        "daterange": "0",
        "questions": {
            "Constantinople": "2",
            "Neither": "19",
            "Istanbul": "51"
        }
    },
    "2": {
        "initial": False,
        "text": "Do any of these exist? Independent Canada, US Territory of Alaska, Tokyo",
        "latlng": [45.4215, -75.6972],
        "daterange": "330–1928",
        "questions": {
            "No": "3",
            "Yes": "11"
        }
    },
    "3": {
        "initial": False,
        "text": "The Holy Roman Empire?",
        "latlng": [50.1109, 8.6821],
        "daterange": "330–1867",
        "questions": {
            "Yes": "end",
            "No": "4"
        }
    },
    "4": {
        "initial": False,
        "text": "The United States?",
        "latlng": [38.9072, -77.0369],
        "daterange": "330–899 or 1806–67",
        "questions": {
            "No": "end",
            "Yes": "5"
        }
    },
    "5": {
        "initial": False,
        "text": "Texas is...",
        "latlng": [31.9686, -99.9018],
        "daterange": "1806–67",
        "questions": {
            "Part of Mexico": "6",
            "Independent": "end",
            "Part of the US": "9"
        }
    },
    "6": {
        "initial": False,
        "text": "Florida is part of...",
        "latlng": [27.9944, -81.7603],
        "daterange": "1806–36",
        "questions": {
            "Spain": "7",
            "The US": "8"
        }
    },
    "7": {
        "initial": False,
        "text": "Paraguay?",
        "latlng": [-23.4425, -58.4438],
        "daterange": "1806–21",
        "questions": {
            "No": "end",
            "Yes": "end"
        }
    },
    "8": {
        "initial": False,
        "text": "Venezuela and/or Ecuador?",
        "latlng": [6.4238, -66.5897],
        "daterange": "1821–36",
        "questions": {
            "No": "end",
            "Yes": "end"
        }
    },
    "9": {
        "initial": False,
        "text": "Does Russia border the Sea of Japan?",
        "latlng": [43.1332, 131.9113],
        "daterange": "1846–67",
        "questions": {
            "No": "10",
            "Yes": "end"
        }
    },
    "10": {
        "initial": False,
        "text": "The US's southern border looks...",
        "latlng": [31.9686, -99.9018],
        "daterange": "1846–58",
        "questions": {
            "Weird": "end",
            "Normal": "end"
        }
    },
    "11": {
        "initial": False,
        "text": "South Africa?",
        "latlng": [-30.5595, 22.9375],
        "daterange": "1868–1928",
        "questions": {
            "No": "12",
            "Yes": "16"
        }
    }
}

next_question_id = "0"


@app.route('/reset')
def reset_question():
    session['next_question_id'] = "0"
    return jsonify({"message": "Question reset to 1"})


@app.route('/question/<question_id>')
def get_question(question_id):
    question_data = questions.get(question_id, {})
    if question_data:
        return jsonify(question_data)
    else:
        return jsonify({"error": "Question not found"}), 404


@app.route('/api/initial-question')
def get_initial_question():
    initial_question_data = questions.get(session.get('next_question_id', "0"), {})
    return jsonify(initial_question_data)


@app.route('/api/response', methods=['POST'])
def handle_response():
    data = request.json
    response = data.get('response')

    current_question_id = session.get('next_question_id', "0")
    current_question = questions.get(current_question_id, {})

    next_question_key = current_question.get('questions', {}).get(response)

    if next_question_key:
        if next_question_key == 'end':
            return jsonify({"message": "End of the questionnaire."})
        else:
            session['next_question_id'] = next_question_key
            next_question_data = questions.get(next_question_key, {})
            return jsonify(next_question_data)
    else:
        return jsonify({"error": "Invalid answer or end of flow"}), 400


if __name__ == "__main__":
    app.run(debug=True)
