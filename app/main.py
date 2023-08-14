import json

import html2text
from env import (
    OPENAI_API_BASE,
    OPENAI_API_SECRET,
    OPENAI_API_TYPE,
    OPENAI_API_VERSION,
    PORT,
)
from flask import Flask, jsonify, request
from flask_cors import CORS
from lang_chain import LangChainAgent
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate

app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def index():
    return ""


@app.route("/health", methods=["GET"])
def health():
    return "OK\n"


@app.route("/getdata", methods=["POST"])
def get_data():

    data = request.get_json()

    print(data)

    customer_name = data["customer_name"]
    agent_name = data["agent_name"]
    type_active = data["type_active"]
    tone_active = data["tone_active"]
    length_active = data["length_active"]
    task = data["task"]

    data = extract_structured_data(
        customer_name, agent_name, type_active, tone_active, length_active, task
    )

    print(data)

    json_data = json.loads(data)

    print(agent_name)

    return jsonify({"success": True, "data": json_data})


# 3. Extract structured info from text via LLM
def extract_structured_data(
    customer_name: str,
    agent_name: str,
    type_active: str,
    tone_active: str,
    length_active: str,
    task: str,
):
    llm = None
    if OPENAI_API_TYPE == "AZURE":
        llm = AzureOpenAI(
            temperature=0,
            openai_api_key=OPENAI_API_SECRET,
            model="gpt-3.5-turbo-0613",
            openai_api_base=OPENAI_API_BASE,
            openai_api_version=OPENAI_API_VERSION,
        )
    else:
        llm = ChatOpenAI(
            temperature=0, openai_api_key=OPENAI_API_SECRET, model="gpt-3.5-turbo-0613"
        )

    length_explanation = ""

    if length_active == "short":
        length_explanation = "a concise"
    elif length_active == "medium":
        length_explanation = "a medium-length"
    elif length_active == "long":
        length_explanation = "a detailed"

    type_prompt = ""
    type_return_object = ""
    if type_active == "email":
        type_prompt = f"please generate {length_explanation} email sent from the Agent to the customer for"
        type_return_object = (
            'Now please return {"subject":"email_subject","body":"email_body"}'
        )
    elif type_active == "note":
        type_prompt = f"please generate {length_explanation} note for the customer to"
        type_return_object = 'Now please return {"body":"note_body"}'
    elif type_active == "text":
        type_prompt = f"please generate {length_explanation} text message sent from the Agent to the customer for"
        type_return_object = 'Now please return {"body":"text_message_body"}'
    elif type_active == "call":
        type_prompt = (
            f"please generate {length_explanation} call log note for the customer to"
        )
        type_return_object = 'Now please return {"body":"call_log_note_body"}'

    template = """
    You are a real estate agent named :{agent_name} 
    who will interact with the customer named :{customer_name} 

    In a {tone_active} tone,{type_prompt} {task}

    {type_return_object} and export in a JSON object format in the same line, 
    return ONLY the JSON object;
    """

    prompt = PromptTemplate(
        input_variables=[
            "customer_name",
            "agent_name",
            "type_prompt",
            "type_return_object",
            "tone_active",
            "task",
        ],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    results = chain.run(
        customer_name=customer_name,
        agent_name=agent_name,
        type_prompt=type_prompt,
        type_return_object=type_return_object,
        tone_active=tone_active,
        task=task,
    )

    return results


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
