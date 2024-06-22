import os
import streamlit as st
import google.generativeai as genai
import random

# Configure the Gemini API
genai.configure(api_key="AIzaSyAZ7myOXP5C5GS4wOq5X4yTstZ2ttH5eos")

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Predefined list of jokes
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "How many programmers does it take to change a light bulb? None. It's a hardware problem.",
    "Why do Java developers wear glasses? Because they don't C#.",
    "What's a programmer's favorite hangout place? Foo Bar.",
    "Why do programmers hate nature? It has too many bugs.",
    "What is a programmer's favorite snack? Computer chips.",
    "Why do Python programmers prefer snake case? Because it's_underscoreable."
]

# Function to generate a coding challenge
def generate_challenge(difficulty):
    difficulty_map = {
        'Easy': 'an easy',
        'Medium': 'a medium',
        'Hard': 'a hard'
    }
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(f"Generate {difficulty_map[difficulty]} coding challenge for beginners in Python.")
    return response.text.strip()

# Function to get AI feedback
def get_feedback(code):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(f"Provide feedback on the following code:\n\n{code}")
    return response.text.strip()

# Function to execute code line-by-line and capture variables
def execute_code_line_by_line(code_lines, current_line, exec_globals):
    exec_locals = {}
    try:
        exec("\n".join(code_lines[:current_line + 1]), exec_globals, exec_locals)
        return exec_locals
    except Exception as e:
        return str(e)

# Initialize session state
if 'points' not in st.session_state:
    st.session_state.points = 0

if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'Easy'

if 'challenge' not in st.session_state:
    st.session_state.challenge = generate_challenge(st.session_state.difficulty)

if 'code_lines' not in st.session_state:
    st.session_state.code_lines = []

if 'current_line' not in st.session_state:
    st.session_state.current_line = 0

if 'exec_globals' not in st.session_state:
    st.session_state.exec_globals = {}

# Header
st.title("LearnCode FunZone")
st.header("Welcome to the Coding Challenges Platform!")
st.subheader("Complete challenges, earn points, and get instant feedback!")

# Difficulty Selection
difficulty = st.selectbox("Select Difficulty", ['Easy', 'Medium', 'Hard'], index=['Easy', 'Medium', 'Hard'].index(st.session_state.difficulty))
if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.challenge = generate_challenge(difficulty)

# Display Coding Challenge
st.markdown("### Your Coding Challenge")
st.write(st.session_state.challenge)

# Code Input
code_input = st.text_area("Your Code:", height=200)
if st.button("Submit Code"):
    st.session_state.code_lines = code_input.split('\n')
    st.session_state.current_line = 0
    st.session_state.exec_globals = {}
    st.success("Code submitted! Start debugging below.")

# Points Display
st.markdown(f"## Your Points: {st.session_state.points}")

# Debugging Section
if st.session_state.code_lines:
    if st.session_state.current_line < len(st.session_state.code_lines):
        current_line_code = st.session_state.code_lines[st.session_state.current_line]
        st.markdown(f"### Line {st.session_state.current_line + 1}")
        st.code(current_line_code)

        # Execute the current line and capture variable states
        exec_locals = execute_code_line_by_line(st.session_state.code_lines, st.session_state.current_line, st.session_state.exec_globals)
        
        # Display current variable states
        st.markdown("### Current Variables")
        st.write(exec_locals)
        
        if st.button("Next Line"):
            st.session_state.current_line += 1

        if st.button("Step In"):
            # Provide more detailed step-in feedback (simulate step-in behavior)
            feedback = get_feedback(current_line_code)
            st.markdown("### Step-In Feedback")
            st.write(feedback)
        
        if st.session_state.current_line > 0 and st.button("Step Out"):
            st.session_state.current_line -= 1
    else:
        st.success("End of code reached. Debugging completed.")

# Generate a new challenge
if st.button("Skip Challenge"):
    st.session_state.challenge = generate_challenge(st.session_state.difficulty)

# Joke of the Day (optional fun feature)
if st.button("Tell me a joke"):
    st.write(random.choice(jokes))
