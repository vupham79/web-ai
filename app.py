import requests
import streamlit as st
import random
import time
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# LLM configuration
messages = [
    (
        "system",
        "You are a helpful assistant that can crawl HTML from provided url and summarize in human readable text. You can add emoji to your messages to make them more engaging. Try to engage the user by suggesting further questions.",
    ),
]
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=st.secrets["GOOGLE_GEMINI_API_KEY"],
)
chain = llm

# Streamlit app
st.title("Website Content Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    messages.append((message["role"], message["content"]))
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


# Streamed response emulator
def response_generator():
    if prompt:
        messages.append(("human", prompt))
        # Check if prompt contains a URL
        if re.search(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            prompt,
        ):
            # Extract the URL from the prompt
            url = re.findall(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                prompt,
            )[0]
            # Respond to the URL
            response = f"Sure! Here is the URL you provided: {url}\n"
            # Request the URL
            html_content_response = requests.get(f"https://r.jina.ai/{url}")
            # Check if the request was successful
            if html_content_response.status_code == 200:
                # Get the response content
                response_content = html_content_response.text
                # Process the response content as needed
                llm_response = chain.invoke(
                    "Summarize the HTML source in human friendly tone:\n"
                    + response_content
                ).content
                # Generate the final response
                response += llm_response
            else:
                response += "Sorry, there was an error processing the URL."
        else:
            response = chain.invoke(messages).content

        messages.append(("assistant", response))
        # Yield each word in the response with a delay
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.02)
    else:
        # Generate a random response
        response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )
        yield response


# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = st.write_stream(response_generator())
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})
