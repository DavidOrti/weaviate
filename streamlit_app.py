import streamlit as st
from utils.funcs import get_query_from_toggles, generative_search


# initialize session state attribute
if 'horizontal' not in st.session_state:
    st.session_state.horizontal = True
    st.session_state.disabled = True
    st.session_state.preset_input = False


# Hero Image
st.image('utils/hero.png')

# Project description
st.title("Generative Shoe Finder")
st.write("Looking for a new pair of trainers is more challenging than running itself?  \nJust type what you want below, :green[Weaviate]'s generative search (RAG) will find the best fit for you")


st.markdown("<br><br>", unsafe_allow_html=True)

if not st.session_state.preset_input:
    user_query = st.text_input(
        label="What are you looking for? Who are you?",
        value="I want some running shoes with zero drop..."
    )

# st.checkbox("Or build from a preset", key="disabled")
st.checkbox("Or build from a preset", key="preset_input")

# Input query as preset
# if not st.session_state.disabled:
if st.session_state.preset_input:

    shoe_type = st.radio(
        "What shoe type are you looking for?",
        ["road :motorway:", "trail :mountain:"],
        index=None,
        #disabled=not st.session_state.disabled,
        horizontal=st.session_state.horizontal
    )

    runner_profile = st.radio(
        "What's your level?",
        ["beginner :chair:", "advanced :rocket:"],
        index=None,
        #disabled=not st.session_state.disabled,
        horizontal=st.session_state.horizontal
    )

    goal = st.radio(
        "What's your goal?",
        ["training :running_shirt_with_sash:", "competition :trophy:", "training and competition :dizzy:"],
        index=None,
        #disabled=not st.session_state.disabled,
        horizontal=st.session_state.horizontal
    )

    shoe_property = st.radio(
        "Any extra wishes?",
        ["lightweight", "cushioned", "stable", "zero drop", "inexpensive", "wide"],
        index=None,
        #disabled=not st.session_state.disabled,
        horizontal=st.session_state.horizontal
    )

    user_query = get_query_from_toggles(
        shoe_type=shoe_type.split(' ')[0] if shoe_type else None,
        runner_profile=runner_profile.split(' ')[0] if runner_profile else None,
        shoe_property=shoe_property if shoe_property else None,
        goal=goal.split(' ')[0] if goal else None
    )

    if user_query:
        st.write(f'Query: "{user_query.strip()}"')


if st.button("Find running shoes!"):
    response_object, response_generated = generative_search(user_query)
    slug = response_object.properties['slug']
    shoe_name = response_object.properties['shoe_name']
    explanation = response_generated
    url = response_object.properties['review_url']

    if slug:
        st.markdown(f'## {shoe_name}')
        st.markdown(explanation)
        st.image(f"data/images/{slug}.jpg")

    st.markdown(f"You can find more info about the {shoe_name} in the [Doctors of Running review]({url}) –where all the reviews for this demo are respectfully sourced from :)")


st.markdown("<br><br><br><br>", unsafe_allow_html=True)

st.caption("Please note that the [review selection](https://github.com/DavidOrti/weaviate/blob/main/data/shoes.json) is *very* limited, so results might be off for some queries with several requests")

st.caption(f"Demo created by [David Ortiz](https://github.com/DavidOrti/weaviate) with :green_heart: from Valencia")
