from typing import List

from utils import token_counter
from core.openai import client as openai_client


def generate_flashcards_usecase(content: str, quantity: int) -> List[dict]:
    generated_flashcards = []
    
    if token_counter(content) > 1.6e4:
        content_slices = []
        #TODO: Adiciona slices
        for piece in content_slices:
            flashcards_list = openai_client.flash_card_generator(prompt=piece,\
                history=generated_flashcards, quantity=quantity)
            generated_flashcards.extend(flashcards_list)
    else:
        generated_flashcards = openai_client.flash_card_generator(prompt=piece,\
            history=generated_flashcards, quantity=quantity)
        
    return generated_flashcards
        
        
