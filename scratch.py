import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_PROJECT_API_KEY"))

def make_api_call():
    base_url = "https://api.open5e.com/v1"
    endpoint = "/classes/"

    url = base_url + endpoint
    response = requests.get(url)
    data = response.json()

    print(data)

def reccomend_class():
    classes_url = "https://api.open5e.com/v1/classes/"
    all_classes = requests.get(classes_url).json().get("results")

    class_summaries = ""
    for dnd_class in all_classes:
        class_summaries += f"""
            {dnd_class.get("name")}: 
            {dnd_class.get("desc")}
        """

    input_yes = "I want a really strong character that can tank and has no spellcasting"
    input_no = "I want a very smart and intellect based character that specialises in spellcasting"

    prompt = f"""
        You are an assistant helping someone pick a class for their Dungeons and Dragons character.
        The message indicating their desires and intent for this character is this:
        {input_no}

        Make a reccomendation for their character class based on the above message and the following class summaries:
        {class_summaries}
    """

    response =  client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": prompt},
    ],
    max_tokens=4000
    )

    return response.choices[0].message.content.strip()

def get_all_classes():
    classes_url = "https://api.open5e.com/v1/classes/"
    all_classes = requests.get(classes_url).json().get("results")

    class_summaries = ""
    for dnd_class in all_classes:
        class_summaries += f"""
            {dnd_class.get("name")}: 
            Hit die: {dnd_class.get("desc")}
        """

    return class_summaries

print(get_all_classes())