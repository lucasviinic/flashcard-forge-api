import os
from time import sleep
from openai import OpenAI
import dotenv
import json
from utils import constants


dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def flash_card_generator(prompt: str, history: str, quantity: int, difficulty: int = 1):
    max_attempt = 3
    attempt = 0

    difficulty_levels = {0: 'fácil', 1: 'médio', 2: 'difícil'}

    while True:
        try:
            model = os.getenv('DEFAULT_MODEL')
            system_prompt = f"""
Você é um gerador de flashcards e apenas um gerador de flashcards. Com base em todo texto que receber, você deve apenas gerar {quantity} ótimos flashcards de grau {difficulty_levels[difficulty]} sobre o conteúdo do texto. Você deve gerar apenas perguntas e respostas contendo o que pode ser encontrado no texto fornecido. Você é um gerador de flashcards e deve gerar apenas flashcards.

----------------------------------------------------

Você deve entregar o resultado no formato JSON. Você SEMPRE deve retornar o resultado no formato JSON, contendo uma lista de flashcards no seguinte formato:

{
  "flashcards": [
        {
            "question": "conteúdo da pergunta contendo no máximo 100 caracteres",
            "answer": "conteúdo da respostas contendo no máximo 100 caracteres"
        }
  ]
}
            """
            system_prompt = f"""
            Você é um gerador de flashcards. Dado o texto de um pdf, crie {quantity} flashcards com pequenas perguntas e respostas
            baseadas no conteúdo do texto do pdf.
            ## A resposta deve SEMPRE ter o formato abaixo:
            {json.dumps(constants.FLASHCARDS_RESPONSE_TEMPLATE)}
            """
            response = client.chat.completions.create(
                model=model,
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
                max_tokens=16383,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={
                    "type": "json_object"
                }
            )

            response = json.loads(response.choices[0].message.content)
            return response

        except Exception as error:
            attempt += 1
            if attempt >= max_attempt:
                return "Error on GPT3: %s" % error
            print('Error on comunicate with OpenAI:', error)
            sleep(1)