import json
import re
from pathlib import Path

import streamlit as st
import weaviate
import weaviate.classes as wvc


def load_info_json() -> dict:
    """Loads main shoe info JSON file"""
    DATA_DIR = Path('data')
    INFO_FILE = 'shoes.json'
    with open(DATA_DIR/INFO_FILE, 'r') as file:
        return json.load(file)


def extract_xml_tag(text: str, tag: str) -> str:
    """Extracts a given XML-like tag from a text"""
    pattern = rf'<{tag}>(.*?)</{tag}>'
    print(pattern)
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def remove_xml_tag(text: str, tag: str) -> str:
    pattern = rf'<{tag}>(.*?)</{tag}>'
    return re.sub(pattern, '', text).strip()


def get_slug(title: str) -> str:
    """Gets slug-like string from model name"""
    return title.lower().replace(' ', '-')


def get_weaviate_client():
    client = weaviate.connect_to_wcs(
        cluster_url=st.secrets["WCS_DEMO_URL"],
        auth_credentials=weaviate.auth.AuthApiKey(st.secrets["WCS_DEMO_RO_KEY"]),
        headers={'X-OpenAI-Api-key': st.secrets["OPENAI_API_KEY"]}
    )
    return client


def get_query_from_toggles(shoe_type: str, runner_profile: str, shoe_property: str, goal: str) -> str:
    """Builds a query from a few selectors"""
    query = 'I want some '
    query += f"{shoe_type} running shoes " if shoe_type else "running shoes "
    query += f"that are {shoe_property} " if shoe_property else ""
    query += f"for a {runner_profile} runner " if runner_profile else ""
    query += f"to be used for {goal}" if goal else ""
    return query


def generative_search(user_query: str):
    try:
        client = get_weaviate_client()
        reviews = client.collections.get('ShoeReviewsDev')

        response = reviews.generate.near_text(
            query=user_query,
            limit=10,
            grouped_task='Recommend a single running shoe among the ones provided as context for the user input query, the one that best adapts to the user needs. Explain briefly and in simple terms, for non-running experts, in just two or three bullet points why you made that recommendation for the user input query. You can use markdown. Please start your response with the full_name of the selected model in the following format: <name>full_name</name>, then the summary of your recommendation.',
            grouped_properties=['shoe_name', 'text'],
            return_metadata=wvc.query.MetadataQuery(distance=True)
        )

    finally:
        client.close()

    return response.generated
