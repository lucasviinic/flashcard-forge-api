import PyPDF2
import tiktoken
import os
import dotenv


dotenv.load_dotenv()

def pdf_to_text(pdf) -> str:
    text = ''
    try:
        with open(pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
    except Exception as e:
        raise RuntimeError(f"Error processing PDF file: {e}")

    return text

def token_counter(text: str) -> int:
    coder = tiktoken.encoding_for_model(os.getenv('DEFAULT_MODEL'))
    token_list = coder.encode(text)
    size = len(token_list)
    
    return size