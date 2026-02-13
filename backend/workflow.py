from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

from backend.prompts import (
    INTENT_PROMPT,
    ENTITY_EXTRACTION_PROMPT,
    RESPONSE_PROMPT,
    VALIDATION_PROMPT
)

def build_workflow():

    llm = ChatOllama(model="mistral", temperature=0.2)
    parser = StrOutputParser()

    intent_chain = (
        ChatPromptTemplate.from_template(INTENT_PROMPT)
        | llm
        | parser
    )

    entity_chain = (
        ChatPromptTemplate.from_template(ENTITY_EXTRACTION_PROMPT)
        | llm
        | parser
    )

    response_chain = (
        ChatPromptTemplate.from_template(RESPONSE_PROMPT)
        | llm
        | parser
    )

    validation_chain = (
        ChatPromptTemplate.from_template(VALIDATION_PROMPT)
        | llm
        | parser
    )

    return intent_chain, entity_chain, response_chain, validation_chain


intent_chain, entity_chain, response_chain, validation_chain = build_workflow()


def run_workflow(user_input):

    intent = intent_chain.invoke({"input": user_input}).strip()

    entities_raw = entity_chain.invoke({"input": user_input})

    try:
        entities = json.loads(entities_raw)
    except:
        entities = {}

    response = response_chain.invoke({
        "input": user_input,
        "intent": intent,
        "entities": entities
    })

    validation_result = validation_chain.invoke({
        "response": response
    }).strip()

    if validation_result.startswith("FAIL"):
        response = response_chain.invoke({
            "input": user_input,
            "intent": intent,
            "entities": entities
        })

        validation_result = validation_chain.invoke({
            "response": response
        }).strip()

    return {
        "intent": intent,
        "entities": entities,
        "response": response,
        "validation": validation_result
    }