import openai
import jira 
import json

# should confluence pages be created for individual tickets or for feature level

#JIRA ticket - story level
#Issue
#Proposed solution - code/psuedocode provided by chatGPT

#Confluence Page - feature level
#Documents all of feature level and decompositions

#keys
with open('keys.json') as f:
    keys = json.load(f)

openai.api_key = keys["gpt4key"]

def main():
    # Feed GPT-4 with the necessary context, tech stack, and parameters
    tech_stack = "Python, Django, React, and PostgreSQL"
    context = f"We are building an AI assistant for high-performing enterprise scrum teams using GPT-4 as an API backend. The assistant is expected to understand the product, recommend a minimum viable product, decompose features into stories, and suggest solutions for each story similar to how an enterprise level agile scrum team would. The tech stack includes {tech_stack}. The stories should last about 1-3 days."

    # Ensure GPT-4 understands the high-level product
    product_description = "Provide a high-level product description here."
    prompt1 = f"{context}\n{product_description}\nDoes GPT-4 understand the high-level product? If not, what additional information is needed?"
    response1 = generate_response(prompt1)

    # If GPT-4 needs more information, ask the user to provide it
    #TODO: Won't the words additional information show up in the response anyway?
    #  We should have it give us a certain output if GPT needs additional information
    if "additional information" in response1.lower():
        additional_info = "User provides additional information."
        context += f"\n{additional_info}"

    # Ask GPT-4 about the minimum viable product and priority features
    prompt2 = f"{context}\nWhat should the minimum viable product look like and what features should be prioritized?"
    response2 = generate_response(prompt2)

    # Decompose prioritized features into stories
    prioritized_features = response2
    prompt3 = f"{context}\nDecompose the following prioritized features into stories: {prioritized_features}"
    response3 = generate_response(prompt3)

    # For each story, get recommendations for solutions
    stories = response3
    prompt4 = f"{context}\nFor each of the following stories, provide recommendations for solutions: {stories}"
    response4 = generate_response(prompt4)

    # Move features, stories, and code recommendations to Confluence
    move_to_confluence(response2, response3, response4)

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

def create_jira_issue(project_key, summary, description, issue_type):
  jira_options = {
      'server': 'https://jira-fc-ai.atlassian.net'
  }
  jira = jira.JIRA(options=jira_options, basic_auth=(keys['ba_name'], keys["ba_key"]))

  issue_dict = {
    'project': {'key': project_key},
    'summary': summary,
    'description': description,
    'issuetype': {'name': issue_type},
  }

  issue = jira.create_issue(fields=issue_dict)
  return issue

def move_to_confluence(features, stories, recommendations):
    # Add code here to move the generated content to Confluence, e.g., using the Confluence REST API
    pass

if __name__ == "__main__":
    main()
