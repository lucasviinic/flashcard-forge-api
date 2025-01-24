FLASHCARDS_RESPONSE_TEMPLATE = {
  "flashcards": [
        {
            "question": "conteúdo da pergunta contendo no máximo 100 caracteres",
            "answer": "conteúdo da respostas contendo no máximo 100 caracteres",
            "opened": False
        }
  ]
}

USER_LIMITS = {
    0: {
        "flashcards_limit": 100,
        "ai_gen_flashcards_limit": 50,
        "subjects_limit": 10
    },
    1: {
        "flashcards_limit": 20000,
        "ai_gen_flashcards_limit": 500,
        "subjects_limit": 1000
    }
}