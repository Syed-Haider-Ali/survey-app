import json
from django.contrib.auth.hashers import make_password

def survey_payload(case):
    data = {}
    if case == 'ideal':
        data = {
    "title":"Pakistan Zindabad",
    "description":"Gathering Information Regarding Election 2024 Acceptance",
    "questions":[
        {
            "question":"How long will you take to do this?",
            "type":1
        },
        {
            "question":"Will you accept Mian sb?",
            "type":1
        },
        {
            "question":"How long will you take to do this",
            "type":2,
            "options":["first one", "second one", "third one", "fourth one"]
        },
        {
            "question":"How long will you take to do this",
            "type":2,
            "options":["fifth one", "sixth one", "seventh one", "eighteth one"]
        },
        {
            "question":"How long will you take to do this",
            "type":2,
            "options":["ninth one", "Tenth one", "Eleventh one", "Twelth one"]
        },
        {
            "question":"How long will you take to do this",
            "type":2,
            "options":["Thirteenth one", "Fourteenth one", "Fifteenth one", "Sixteenth one"]
        }
    ]
}

    elif case == 'lt_5':
        data = {
            "title": "Pakistan Zindabad",
            "description": "Gathering Information Regarding Election 2024 Acceptance",
            "questions": [
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
            ]
        }

    elif case == 'gt_10':
        data = {
            "title": "Pakistan Zindabad",
            "description": "Gathering Information Regarding Election 2024 Acceptance",
            "questions": [
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
            ]
        }

    elif case == 'dropdown_questions_with_no_option':
        data = {
            "title": "Pakistan Zindabad",
            "description": "Gathering Information Regarding Election 2024 Acceptance",
            "questions": [
                {
                    "question": "How long will you take to do this?",
                    "type": 2
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 2
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["ninth one", "Tenth one", "Eleventh one", "Twelth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["Thirteenth one", "Fourteenth one", "Fifteenth one", "Sixteenth one"]
                }
            ]
        }

    return data

def submit_survey_form_payload(survey_id):
    data = {
        "survey_form": survey_id,
        "answers": [
            {
                "question": 1,
                "descriptive_answer": "In about 30 mins"
            },
            {
                "question": 2,
                "descriptive_answer": "Obviously"
            },
            {
                "question": 3,
                "chosen_answer": 1
            },
            {
                "question": 4,
                "chosen_answer": 5
            },
            {
                "question": 5,
                "chosen_answer": 9
            },
            {
                "question": 6,
                "chosen_answer": 14
            }
        ]
    }
    json_data = json.dumps(data)
    return json_data

def user_obj():
    user_data = {
        "first_name": "haider",
        "email": "haider@gmail.com",
        "username": "haider@gmail.com",
        "password": make_password("admin1234"),
        "is_active": True,
        "is_locked": False
    }
    return user_data