import openai
import streamlit as st
import os
import json
from jira import JIRA

#step1
# overall project gets created based on what GPT provides an MVP
# GPT then comes up with features ie swimlanes which are also validated by user - this needs to be ranked according to Priority inputs 
# From there, we have GPT decompose each feature into specific TICKETS
# Each ticket consists of Project, Summary (gen by GPT), Type (Task), Status (ToDo), Description (long form summary gen by GPT), Priority (we add in inputs)
# 

#TODO: if a user does not like a portion, add a button and a input that sends back to GPT to redo output

#keys
with open('keys.json') as f:
    keys = json.load(f)

openai.api_key = keys["gpt4key"]

def main():
    st.title("AI Assistant for Scrum Teams")
    # what is the problem you are trying to solve 
    problem_statement = st.text_input("What is the problem you are trying to solve?")
    # what you are building
    product_description = st.text_input("Enter a high-level product description. What are you trying to build? What is the MVP in your head?:")
    # what is the end-user doing currently
    end_user_current_sol = st.text_input("What is the end-user doing currently")
    # provide a tech stack if you have one in mind
    tech_stack = st.text_input("Provide a tech stack if you have one in mind")
    submit_button = st.button("Submit")
    context = f"""
        We are building an AI assistant for high-performing enterprise scrum teams using GPT-4 as an API backend.
        When responding to questions: respond in the style of 
            Marty Cagan - Author of "Inspired: How to Create Tech Products Customers Love" and founder of the Silicon Valley Product Group,
            Eric Ries - Author of "The Lean Startup" and founder of the Lean Startup movement,
            Steve Blank - Author of "The Four Steps to the Epiphany" and pioneer of the Lean Startup movement,
            Don Norman - Author of "The Design of Everyday Things" and former Vice President of Apple's Advanced Technology Group,
            Clayton Christensen - Author of "The Innovator's Dilemma" and a professor at Harvard Business School,
        Problem Statement: {problem_statement}
        High-Level Product Description: {product_description}
        Current End-User Solution: {end_user_current_sol}
        Potential Tech-Stack: {tech_stack}
        """
    
    output = st.container()
    r1 = ""
    if submit_button and product_description:
        prompt1 = f"{context}\nUsing the high-level product description, please provide a long detailed description of a potential minimum viable product that can be built"
        response1 = generate_response(prompt1)
        output.write(response1)
        print(response1)
        r1 = response1
    
    output2 = st.container()
    r2 = ""
    if st.button("Generate MVP and Features"): 
        prompt2 = f"{context}\nCan you give me a feature backlog with some priority to build this MVP:\n{r1}.\n Just limit it to top 2 features for now. Think of features as epics/features that would be captured in jira. In the next step i will ask you to decompose each of these features into user stories"
        response2 = generate_response(prompt2)
        st.write(response2)
        print(response2)
        r2 = response2

    output3 = st.container()
    r3 = ""
    if st.button("Decompose Features into Stories"):
        prompt3 = f"{context}\nLet's decompose each feature provided here:\n{r2}\ninto tasks. Only provide 2 tasks per feature."
        response3 = generate_response(prompt3)
        st.write(response3)
        print("r3")
        print(response3)
        r3 = response3
        parse_ticket_info(response3)
    #gen_ticket(summary, description)



    output4 = st.container()
    if st.button("Generate Recommendations for Stories"):
        prompt4 = f"{context}\nFor each of the following stories, provide recommendations for solutions:"
        response4 = generate_response(prompt4)
        st.write(response4)

def generate_response(prompt, max_tokens=3000):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

def gen_ticket(summary, description):
    jira_connection = JIRA(
        basic_auth=(keys["ba_email"], keys["ba_key"]),
        server='https://jira-fc-ai.atlassian.net/'
    )
    issue_dict = {
        'project': {'key': "FIRST"},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Task'},
    }
    jira_connection.create_issue(issue_dict)
    print("issue created")

def parse_ticket_info(r3):
    print("r3 in parse")
    print(r3)
    lines = r3.split("\n")
    print(len(lines))
    tickets = []
    for i in range(0, len(lines)):
        line = lines[i]
        # Split the line by the colon at the beginning of the sentence
        split_line = line.split(". ", 1)
        print(split_line)
        summary = split_line[1]
        # If the line starts with a number, add the sentence to the array
        desc = generate_response(f"Create a 3-4 sentence paragraph that expands this task\n{summary}. Do not include any prose")
        print("this is the desc", desc)
        gen_ticket(summary=summary, description=desc)
    print(tickets)


if __name__ == "__main__":
    main()
    print("complete")
