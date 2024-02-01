import os
from time import sleep
from openai import OpenAI
import dotenv


dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def flash_card_generator(prompt: str, history: str, quantity: int):
    max_attempt = 1
    attempt = 0

    while True:
        try:
            model='gpt-3.5-turbo-16k'
            system_prompt=f"""
            Você é um gerador de flashcards. Dado o texto de um pdf, crie {quantity} flashcards com pequenas perguntas e respostas
            baseadas no conteúdo do texto do pdf.
            ## Formato esperado (JSON com {quantity} flashcards):
            {{
                \"flashcards\": [
                    {{
                        \"question\": \"texto com a pergunta\",
                        \"answer\": \"texto com a resposta\"
                    }}
                ]
            }}
            ## Histórico de flashcards para evitar repetições:
            {history}
            """
            response = client.chat.completions.create(messages=[
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
            model=model)
            return response
        except Exception as erro:
            attempt += 1
            if attempt >= max_attempt:
                return "Error on GPT3: %s" % erro
            print('Error on comunicate with OpenAI:', erro)
            sleep(1)