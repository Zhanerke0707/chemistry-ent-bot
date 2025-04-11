import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def explain_answer(question, user_answer, correct_answer):
    prompt = f"""Ученик ответил на вопрос по химии:
Вопрос: {question}
Ответ ученика: {user_answer}
Правильный ответ: {correct_answer}

Объясни, почему правильный ответ верен, а ответ ученика — нет (если он ошибся)."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
