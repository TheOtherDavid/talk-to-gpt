#!/usr/bin/env python3

import openai
import os
import json
import random
from dotenv import load_dotenv

load_dotenv()

def get_gpt_response(prompt):
    api_key = os.environ['API_KEY']
    openai.api_key = api_key

    messages = [
        {"role": "system", "content": "You are a assistant who gets the most important information across in about one paragraph."},
    ]
    
    message = prompt

    messages.append({"role": "user", "content": message})
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.5
    )
    answer = chat_completion.choices[0].message.content
    return answer

if __name__ == '__main__':
    response = get_gpt_response()
    