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


def flow(prompt):
    intent = find_intent(prompt), "TODO: implement chat summarization"
    response = intent
    if intent == "Create":
        response = create_char(prompt)
    
    return response


def find_intent(prompt):
    prompt = f"""
        Given the following message, classify the intent of the message.
        Provide your classification based on the given categories only, using only the words: create, optimize, select, or other.
        Your classification must strictly be one of the following categories:
        - Create: Creating a DnD character from scratch
        - Select: Selecting specific traits of a character with others already set, usually for some desired outcome
        - Level Up: Leveling an existing character up and making leveling decisions.
        - Other: Anything other than creating or refining a DnD character

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


def create_char(prompt):
    char_class = choose_class(prompt)



def choose_class(prompt):
    
    
    prompt = f"""
        Given the following message, choose a class for a dnd character.
        Provide your class based on the given categories only, using only the words: create, optimize, select, or other.
        Your classification must strictly be one of the following categories:
        - Create: Creating a DnD character from scratch
        - Select: Selecting specific traits of a character with others already set, usually for some desired outcome
        - Level Up: Leveling an existing character up and making leveling decisions.
        - Other: Anything other than creating or refining a DnD character

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
