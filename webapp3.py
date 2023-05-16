# -*- coding: utf-8 -*-
"""WebApp3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tTsxHXIYswwhB8mqofMM-wuDa68kTLsJ
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import openai

openai.api_key = st.secrets["api_key"]

# Define the function to generate the Google ad
def generate_ad(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string
    description = soup.find('meta', attrs={'name': 'description'})['content']
    ad = f"Buy {title} today! {description}"
    return ad

# Define the function to suggest 10 keywords
def suggest_keywords(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(strip=True)
    words = re.findall(r'\b\w+\b', text)
    keyword_list = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Suggest 10 keywords for {url}: {text}",
        max_tokens=50,
        n=10,
        stop=None,
        temperature=0.5,
    )
    keywords = [choice.text for choice in keyword_list.choices]
    return keywords

# Define the function to generate a summary
def generate_summary(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(strip=True)
    summary = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following article: {text}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return summary.choices[0].text

# Define the main function that will display the app in Streamlit
def app():
    # Set the title of the app
    st.title("Campaign Generator")

    # Ask user for the URL
    url = st.text_input("Enter a webpage URL:")

    # Check if the user has entered a URL
    if url:
        # Display the Google ad
        st.write("## Google Ad")
        ad = generate_ad(url)
        st.write(ad)

        # Display the suggested keywords
        st.write("## Suggested Keywords")
        keywords = suggest_keywords(url)
        for i, keyword in enumerate(keywords):
            st.write(f"{i+1}. {keyword}")

        # Display the summary
        st.write("## Summary")
        summary = generate_summary(url)
        st.write(summary)
    else:
        st.write("Please enter a URL.")

# Run the app
if __name__ == '__main__':
    app()
