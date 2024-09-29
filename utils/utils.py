from typing import List
import PyPDF2
import tiktoken
import os
import dotenv


dotenv.load_dotenv()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def pdf_to_text(pdf) -> str:
    pdf.seek(0, os.SEEK_END)  # Move o ponteiro para o final do arquivo
    file_size = pdf.tell()    # Obtém a posição do ponteiro, que é o tamanho do arquivo
    pdf.seek(0)               # Move o ponteiro de volta para o início do arquivo

    if file_size > MAX_FILE_SIZE:
        raise RuntimeError(f"O arquivo PDF excede o limite de 5MB.")

    text = ''
    try:
        reader = PyPDF2.PdfReader(pdf)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    except Exception as e:
        raise RuntimeError(f"Error processing PDF file: {e}")

    return text

def fragment_text(text_content: str) -> List[str]:
    token_count = token_counter(text_content)
    max_token = int(os.getenv('MAX_TOKENS'))
    
    if token_count <= max_token:
        return [text_content]
    
    num_parts = (token_count // max_token) + (1 if token_count % max_token else 0)
    tokens_per_part = token_count // num_parts

    words = text_content.split()
    fragments = [
        " ".join(words[i:i+tokens_per_part]) for i in range(0, len(words), tokens_per_part)
    ]

    return fragments

def token_counter(text: str) -> int:
    coder = tiktoken.encoding_for_model('gpt-4-turbo')
    token_list = coder.encode(text)
    size = len(token_list)
    
    return size