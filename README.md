# Welcome to Web AI

## Prerequisites

Python >= 3.8 and =< 3.12

## 1. Install Dependencies

`$ pip install -r requirements.txt`

## 2. Environment Variables

`$ cp .streamlit/secrets.toml.example > .streamlit/secrets.toml`

From `.streamlit/secrets.toml`, please replace your own Gemini API Key (https://ai.google.dev/gemini-api/docs/api-key). You can easily have one and it is free and no credit card is required upfront.

## 3. Start Application

`$ streamlit run app.py`

The application should now automatically open on your browser in URL http://localhost:8501/

## How it works

If your message does not include any URL within, the AI bot will not try to crawl any HTML source but will answer with its own knowledge base. Otherwise, it will extract the URL within and crawl the HTML source by Jina AI (https://jina.ai/reader/), then summarize the content by Gemini AI.

## Tech Stacks

#### Streamlit (https://streamlit.io/)

#### Google Gemini AI (https://ai.google.dev/)

#### Jina AI (https://jina.ai/)
