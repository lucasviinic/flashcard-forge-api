import os
from time import sleep
from openai import OpenAI
import dotenv
import json
from utils import constants


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def flash_card_generator(prompt: str, history: list, quantity: int, difficulty: int = 1):
    model = os.getenv('DEFAULT_MODEL')
    max_attempt = 3
    attempt = 0

    difficulty_levels = {-1: 'fácil', 0: 'médio', 1: 'difícil', 2: 'muito difícil'}

    while True:
        try:
            system_prompt = f"""
            ## Você é um gerador de flashcards e apenas um gerador de flashcards. Com base em todo texto que receber, você deve apenas gerar {quantity} ótimos flashcards de grau {difficulty_levels[difficulty]} sobre o conteúdo do texto, não faça perguntas triviais, apenas perguntas de nível abordado em provas. Você deve gerar apenas perguntas e respostas contendo o que pode ser encontrado no texto fornecido. Você é um gerador de flashcards e deve gerar apenas flashcards.
            ## SEMPRE que houver exemplos no texto, ou algo do tipo, não responda sobre o exemplo e sim sobre o assunto, SEMPRE sobre o assunto abordado no texto.
            ## Você SEMPRE deve criar os flashcards com perguntas e respostas bem elaboradas (nada simples e bobo).
            ## Você SEMPRE deve gerar {quantity} fleshcards. Gere exatamente {quantity} flashcards. Não gere nem mais nem menos do que {quantity}, gere exatamente {quantity} flashcards.
            ## Certifique-se de ter criado exatamente {quantity} flashcards. Deve ter exatamente {quantity} flashcards.
            ## Você SEMPRE deve entregar o resultado no formato JSON. Você SEMPRE deve retornar o resultado no formato JSON, contendo uma lista de flashcards no seguinte formato:
            {json.dumps(constants.FLASHCARDS_RESPONSE_TEMPLATE)}
            ## Abaixo, está o histórico de flashcards gerados (caso haja conteúdo abaixo, não repita)
            {str(history)}
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
                temperature = 1,
                max_tokens = int(os.getenv('MAX_TOKENS')),
                top_p = 1,
                frequency_penalty = 0,
                presence_penalty = 0,
                response_format = {
                    "type": "json_object"
                }
            )

            response = json.loads(response.choices[0].message.content)
            flashcards = response['flashcards']
            
            return flashcards

        except Exception as error:
            attempt += 1
            if attempt >= max_attempt:
                return f"Error on model {model}: %s" % error
            sleep(1)