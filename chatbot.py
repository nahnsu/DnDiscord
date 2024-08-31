import os
import logging
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

client = OpenAI(api_key=os.getenv("OPENAI_PROJECT_API_KEY"))

def list_available_models():
    # List all models available to the API key
    models = client.models.list()
    # Print the names of all available models
    for model in models.data:
        print(model.id)


def count_tokens(messages, model="gpt-4"):
    """Calculate the number of tokens used in a list of messages."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = 0
    for message in messages:
        tokens += len(encoding.encode(message['role'])) + len(encoding.encode(message['content']))
    logging.info("Estimated number of tokens: " + str(tokens))
    return tokens


def flow(prompt, chat_history):
    return find_intent(prompt, chat_history), "TODO: implement chat summarization"
    # token_limit = 4096  # Token limit for gpt-4 is
    # while count_tokens(chat_history) > token_limit:
    #     chat_history.pop(0)

    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=chat_history
    # )

    # assistant_response = response.choices[0].message.content.strip()
    # chat_history.append({"role": "assistant", "content": assistant_response})
    
    # # Extract and return the generated text
    # return assistant_response, chat_history


def find_intent(prompt, chat_history):
    prompt = f"""
        Given the following chat history and message, classify the intent of the message.
        Provide your classification based on the given categories only, using only the words: create, optimize, select, or other.
        Your classification must strictly be one of the following categories:
        - Create: Creating a DnD character from scratch
        - Select: Selecting specific traits of a character with others already set, usually for some desired outcome
        - Level Up: Leveling an existing character up and making leveling decisions.
        - Other: Anything other than creating or refining a DnD character

        Chat History:
        {chat_history}

        Message:
        {prompt}
    """

    response =  client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
        ],
        max_tokens=4000
    )
    logging.info("Intent: " + response.choices[0].message.content.strip())
    intent = response.choices[0].message.content.strip()
    return intent
    # if intent == "create":
    #     return create_char(prompt, chat_history)
    # if intent == "other":
    #     return bad_intent_breaker(prompt, chat_history)


def create_char(prompt, chat_history):
    prompt = """
        Given the following chat history and message, help create a DnD character from scratch

        Chat History:
        {chat_history}

        Message:
        {prompt}
    """

    response =  client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
        ],
        max_tokens=4000
    )

    return response.choices[0].message.content.strip()



def bad_intent_breaker(prompt, chat_history):
    return "I can't help you with that. I'm just here to help you make DnD characters"
