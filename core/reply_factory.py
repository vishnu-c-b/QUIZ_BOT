
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
   
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    
    if current_question_id is None:
        
        return True, "" #Initial CASE

  
    answers = session.get("answers", {})
    answers[current_question_id] = answer
    session["answers"] = answers
    return True, ""
       

def get_next_question(current_question_id):
    
    index = 0 if current_question_id is None else current_question_id + 1

    if index < len(PYTHON_QUESTION_LIST):
        next_question_data = PYTHON_QUESTION_LIST[index]
        return f"{next_question_data['question_text']}\nOptions: {', '.join(next_question_data['options'])}", index
    else:
        return None, None
   


def generate_final_response(session):

    answers = session.get("answers", {})
    score = 0
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        correct_answer = question["answer"]
        user_answer = answers.get(i)

        if user_answer == correct_answer:
            score += 1

    total = len(PYTHON_QUESTION_LIST)
    return f"You've completed the quiz! Your score: {score}/{total}."
   


