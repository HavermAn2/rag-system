from ollama import chat
from ollama import ChatResponse
from app.storage.prompts import SYSTEM_PROMPT

def llm(chunks:list,user_query):
    response: ChatResponse = chat(
    model='qwen3:4b-instruct',
    messages=[
        {'role': 'system',
        'content': SYSTEM_PROMPT,},
        {
            
        'role': 'user',
        'content': f"""Context: {chunks}  Question: {user_query}""",
        },
    ],
    )
    return response.message.content
