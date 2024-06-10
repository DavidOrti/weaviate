
import os

import weaviate
import weaviate.classes as wvc
from dotenv import load_dotenv


def get_weaviate_client():
    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WCS_DEMO_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCS_DEMO_RO_KEY")),
        headers={'X-OpenAI-Api-key': os.getenv("OPENAI_API_KEY")}
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
        reviews = client.collections.get('ShoeReviews')

        response = reviews.generate.near_text(
            query=user_query,
            limit=1,  # to keep query and text generation fast and simple
            grouped_task='Recommend the running shoe for which a snippet of text is provided, focusing on what is mentioned there. Very briefly explain why, in just two or three bullet points. You can use markdown. Do not return the shoe name as a bullet point, title or similar.',
            grouped_properties=['shoe_name', 'text'],
            return_metadata=wvc.query.MetadataQuery(distance=True)
        )
        #print(response.generated)

    finally:
        client.close()

    return response.objects[0], response.generated
