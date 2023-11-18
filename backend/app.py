from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


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
    },
    "12": {
        "initial": False,
        "text": "Rhodesia?",
        "latlng": [-19.0154, 29.1549],
        "daterange": "1868–1910",
        "questions": {
            "No": "13",
            "Yes": "15"
        }
    },
    "13": {
        "initial": False,
        "text": "Is Bolivia landlocked?",
        "latlng": [-16.2902, -63.5887],
        "daterange": "1868–95",
        "questions": {
            "No": "14",
            "Yes": "end"
        }
    },
    "14": {
        "initial": False,
        "text": "\"Buda\" and \"Pest\" or \"Budapest\"?",
        "latlng": [47.4979, 19.0402],
        "daterange": "1868–84",
        "questions": {
            "Buda and Pest": "end",
            "Budapest": "end"
        }
    },
    "15": {
        "initial": False,
        "text": "Is Norway part of Sweden?",
        "latlng": [60.4720, 8.4689],
        "daterange": "1895–1910",
        "questions": {
            "Yes": "end",
            "No": "end"
        }
    },
    "16": {
        "initial": False,
        "text": "Austria-Hungary?",
        "latlng": [47.5162, 14.5501],
        "daterange": "1910–28",
        "questions": {
            "Yes": "17",
            "No": "18"
        }
    },
    "17": {
        "initial": False,
        "text": "Albania?",
        "latlng": [41.1533, 20.1683],
        "daterange": "1910–18",
        "questions": {
            "No": "end",
            "Yes": "end"
        }
    },
    "18": {
        "initial": False,
        "text": "Leningrad?",
        "latlng": [59.9343, 30.3351],
        "daterange": "1918–28",
        "questions": {
            "No": "end",
            "Yes": "end"
        }
    },
    "19": {
        "initial": False,
        "text": "Does the Ottoman Empire exist?",
        "latlng": [39.9334, 32.8597],
        "daterange": "Inconclusive",
        "questions": {
            "Yes": "2",
            "No": "20"
        }
    },
    "20": {
        "initial": False,
        "text": "The Soviet Union?",
        "latlng": [55.7558, 37.6173],
        "daterange": "1299- or 1922+",
        "questions": {
            "Yes": "21",
            "No": "22"
        }
    },
    "21": {
        "initial": False,
        "text": "Saudi Arabia?",
        "latlng": [23.8859, 45.0792],
        "daterange": "1922–91",
        "questions": {
            "Yes": "52",
            "No": "end"
        }
    },
    "22": {
        "initial": False,
        "text": "North Korea?",
        "latlng": [40.3399, 127.5101],
        "daterange": "1299- or 1922 (November 1–December 28) or 1991+",
        "questions": {
            "Yes": "69",
            "No": "23"
        }
    },
    "23": {
        "initial": False,
        "text": "Saint Trimble's Island",
        "latlng": [0, 0],
        "daterange": "1299- or 1922 (November 1–December 28)",
        "questions": {
            "No": "24",
            "Yes": "end"
        }
    },
    "24": {
        "initial": False,
        "text": "Is Jan Mayen part of the kingdom of Norway?",
        "latlng": [70.9820, -8.4088],
        "daterange": "1299- or 1922 (November 1–December 28)",
        "questions": {
            "Not yet": "2",
            "What?": "25",
            "Yes": "53"
        }
    },
    "25": {
        "initial": False,
        "text": "Can you see the familiar continents?",
        "latlng": [0, 0],
        "daterange": "",
        "questions": {
            "Yes": "26",
            "No": "32"
        }
    },
    "26": {
        "initial": False,
        "text": "This sounds like a physical map or satellite photo.",
        "latlng": [0, 0],
        "daterange": "Map of the Earth",
        "questions": {
            "Yes, that's it": "27"
        }
    },
    "27": {
        "initial": False,
        "text": "Is Lake Chad missing?",
        "latlng": [13.4696, 14.0150],
        "daterange": "Topographical map or satellite image of the Earth",
        "questions": {
            "No": "28",
            "Yes": "31"
        }
    },
    "28": {
        "initial": False,
        "text": "How far east do the American prairies reach?",
        "latlng": [39.3813, -98.2016],
        "daterange": "1970s-",
        "questions": {
            "Indiana": "end",
            "The Mississippi": "end",
            "Nebraska": "29",
            "What prairies?": "30"
        }
    },
    "29": {
        "initial": False,
        "text": "Is there a big lake in the middle of Southern California? (created by mistake)",
        "latlng": [35.3733, -119.0187],
        "daterange": "1860s–1910s",
        "questions": {
            "No": "end",
            "Yes": "end"
        }
    },
    "30": {
        "initial": False,
        "text": "Is there a big lake in the middle of Ghana? (created on purpose)",
        "latlng": [7.9465, -1.0232],
        "daterange": "1920s–1970s",
        "questions": {
            "No": "end",
            "Yes": "end"
        }
    },
    "31": {
        "initial": False,
        "text": "Is the Aral Sea missing?",
        "latlng": [45.0833, 60.0833],
        "daterange": "1970s+",
        "questions": {
            "No": "end",
            "Yes": "end"
        }
    },
    "32": {
        "initial": False,
        "text": "Rivers \"Sirion\" or \"Anduin\"?",
        "latlng": [0, 0],
        "daterange": "Not a map of the Earth",
        "questions": {
            "Yes": "33",
            "No": "37"
        }
    },
    "33": {
        "initial": False,
        "text": "Mordor?",
        "latlng": [0, 0],
        "daterange": "Map of Middle-earth",
        "questions": {
            "No": "34",
            "Yes": "35"
        }
    },
    "34": {
        "initial": False,
        "text": "Beleriand?",
        "latlng": [0, 0],
        "daterange": "S.A. c. 1000-",
        "questions": {
            "Yes": "end",
            "No": "end"
        }
    },
    "35": {
        "initial": False,
        "text": "Númenor?",
        "latlng": [0, 0],
        "daterange": "S.A. c. 1000+",
        "questions": {
            "Yes": "end",
            "No": "36"
        }
    },
    "36": {
        "initial": False,
        "text": "The forest east of the Misty Mountains is...",
        "latlng": [0, 0],
        "daterange": "S.A. 3319+",
        "questions": {
            "Greenwood the Great": "end",
            "Mirkwood": "end",
            "The Wood of Greenleaves": "end"
        }
    }
}

@app.route('/question/<question_id>')
def get_question(question_id):
    question_data = questions.get(question_id, {})
    if question_data:
        return jsonify(question_data)
    else:
        return jsonify({"error": "Question not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)