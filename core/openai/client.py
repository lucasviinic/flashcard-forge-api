import os
from time import sleep
from openai import OpenAI
import dotenv
import json
from utils import constants


dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def flash_card_generator(prompt: str, history: str, quantity: int):
    max_attempt = 3
    attempt = 0

    while True:
        try:
            model = os.getenv('DEFAULT_MODEL')
            system_prompt = f"""
            Você é um gerador de flashcards. Dado o texto de um pdf, crie {quantity} flashcards com pequenas perguntas e respostas
            baseadas no conteúdo do texto do pdf.
            ## A resposta deve SEMPRE ter o formato abaixo:
            {json.dumps(constants.FLASHCARDS_RESPONSE_TEMPLATE)}
            """
            response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model=model
            )

            response = json.loads(response.choices[0].message.content)
            return response

        except Exception as error:
            attempt += 1
            if attempt >= max_attempt:
                return "Error on GPT3: %s" % error
            print('Error on comunicate with OpenAI:', error)
            sleep(1)