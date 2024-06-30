import streamlit as st
from openai import OpenAI
import os

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="123",
)



def generate_question(topic): #in this we use a finetune model from hf to genrate question
    response = client.chat.completions.create(
        model="models/finetune_model.gguf",
        messages=[
            {"role": "system", "content": "You are an AI assistant that generates questions."},
            {"role": "user", "content": f"Generate a random question about {topic}."}
        ]
    )
    return response.choices[0].message.content

def evaluate_answer(question, user_answer): #in this we use a finetune model from hf to check the answers
    response = client.chat.completions.create(
        model="models/finetune_model.gguf",
        messages=[
            {"role": "system", "content": "You are an AI assistant that evaluates answers."},
            {"role": "user", "content": f"Question: {question}\nUser's answer: {user_answer}\nIs this answer correct? Respond with 'Correct' or 'Incorrect' and provide a brief explanation."}
        ]
    )
    return response.choices[0].message.content

def main(): # user interface using srteamlit 
    st.title("Generative_AI Q&A App")

    
    topic = st.selectbox("Select a topic:", ["Geography", "Health", "Sports"]) # user will chose the topic for questions

    
    if 'question' not in st.session_state or st.button("Generate New Question"):
        st.session_state.question = generate_question(topic)

    st.write("Question:", st.session_state.question)


    user_answer = st.text_input("Your answer:")

    
    
    if st.button("Submit Answer"):
        if user_answer:
            evaluation = evaluate_answer(st.session_state.question, user_answer)
            st.write("Evaluation:", evaluation)
        else:
            st.write("Please provide an answer before submitting.")

if __name__ == "__main__":
    main()