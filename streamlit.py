import openai
import streamlit as st
import os
import json

#keys
with open('keys.json') as f:
    keys = json.load(f)

openai.api_key = keys["gpt4key"]

def main():
    st.title("AI Assistant for Scrum Teams")

    product_description = st.text_input("Enter a high-level product description:")
    
    if product_description:
        context = f"""
        We are building an AI assistant for high-performing enterprise scrum teams using GPT-4 as an API backend.
        The assistant is expected to understand the product, recommend a minimum viable product, decompose features into stories, and suggest solutions for each story.
        The tech stack includes Python, Django, React, and PostgreSQL. The stories should last about 1-3 days.
        """
        
        prompt1 = f"{context}\n{product_description}\nDoes GPT-4 understand the high-level product? If not, what additional information is needed?"
        response1 = generate_response(prompt1)
        st.write(response1)

        if st.button("Generate MVP and Features"):
            prompt2 = f"{context}\nWhat should the minimum viable product look like and what features should be prioritized?"
            response2 = generate_response(prompt2)
            st.write(response2)

            if st.button("Decompose Features into Stories"):
                prompt3 = f"{context}\nDecompose the following prioritized features into stories: {response2}"
                response3 = generate_response(prompt3)
                st.write(response3)

                if st.button("Generate Recommendations for Stories"):
                    prompt4 = f"{context}\nFor each of the following stories, provide recommendations for solutions: {response3}"
                    response4 = generate_response(prompt4)
                    st.write(response4)

def generate_response(prompt, max_tokens=100):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

if __name__ == "__main__":
    print("complete")
