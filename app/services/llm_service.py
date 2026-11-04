from ollama import chat
from ollama import ChatResponse


def llm(chunks:list):
    response: ChatResponse = chat(
    model='qwen3:4b-instruct',
    messages=[
        {
        'role': 'user',
        'content': f'You are LLM for RAG-system. Your main task is to generate a readable answer for users from chunks, dont add something from yourself, only clier answer. Here they are:{chunks} ?',
        },
    ],
    )
    return response.message.content
