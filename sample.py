import streamlit as st
import google.generativeai as genai
import os
import json

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

# File to store generated challenges
GENERATED_CHALLENGES_FILE = 'generated_challenges.json'

# Load generated challenges
if os.path.exists(GENERATED_CHALLENGES_FILE):
    with open(GENERATED_CHALLENGES_FILE, 'r') as file:
        generated_challenges = json.load(file)
else:
    generated_challenges = []

# Function to generate a coding challenge
def generate_challenge(difficulty, challenge_type):
    difficulty_map = {
        'Easy': 'an easy',
        'Medium': 'a medium',
        'Hard': 'a hard'
    }
    type_map = {
        'Arrays': 'using arrays',
        'Dictionaries': 'using dictionaries',
        'Coordinates': 'using coordinates',
        'Strings': 'using strings',
        'Linked Lists': 'using linked lists',
        'Trees': 'using trees',
        'Graphs': 'using graphs',
        'Dynamic Programming': 'using dynamic programming'
    }

    # Check if the challenge has been generated before
    for challenge in generated_challenges:
        if challenge['difficulty'] == difficulty and challenge['type'] == challenge_type:
            return challenge['text']

    # Generate a new challenge if not found
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(
        f"Generate {difficulty_map[difficulty]} coding challenge for beginners in Python {type_map[challenge_type]}. "
        f"Include only the description, sample input, and sample output. Do not generate any solutions. "
        f"Give hints such as what functions or methods to use."
    )
    challenge_text = response.text.strip()

    # Store the new challenge
    new_challenge = {
        'difficulty': difficulty,
        'type': challenge_type,
        'text': challenge_text
    }
    generated_challenges.append(new_challenge)

    with open(GENERATED_CHALLENGES_FILE, 'w') as file:
        json.dump(generated_challenges, file)

    return challenge_text

# Function to get AI feedback
def get_feedback(code, challenge):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(
        f"Evaluate the correctness of this Python code based on the following challenge:\n{challenge}\n\nCode:\n{code}\nIf the code is correct or acceptable, include the string 'Good Job!' in your response."
    )
    return response.text.strip()

# Function to get AI solution
def get_solution():
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(
        f"Generate the solution for this coding challenge. When using more advanced methods and functions, provide more comments to guide the users:\n{st.session_state.challenge}"
    )
    return response.text.strip()

# Initialize session state
if 'points' not in st.session_state:
    st.session_state.points = 0

if 'difficulty' not in st.session_state:
    st.session_state.difficulty = None

if 'challenge_type' not in st.session_state:
    st.session_state.challenge_type = None

if 'challenge' not in st.session_state:
    st.session_state.challenge = None

if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

if 'solution_revealed' not in st.session_state:
    st.session_state.solution_revealed = False

# Select challenge type
st.markdown("## Select Challenge Type")
challenge_type = st.selectbox(
    "Choose the type of coding challenge:",
    ['Arrays', 'Dictionaries', 'Coordinates', 'Strings', 'Linked Lists', 'Trees', 'Graphs', 'Dynamic Programming']
)

# Select difficulty
st.markdown("## Select Difficulty")
difficulty = st.selectbox(
    "Choose the difficulty of the challenge:",
    ['Easy', 'Medium', 'Hard']
)

# Button to generate a challenge
if st.button("Generate Challenge"):
    st.session_state.difficulty = difficulty
    st.session_state.challenge_type = challenge_type
    st.session_state.challenge = generate_challenge(difficulty, challenge_type)
    st.session_state.solution_revealed = False

# Display the challenge and solution if solution is revealed
if st.session_state.challenge:
    if st.session_state.solution_revealed:
        st.markdown(f"## Current Challenge ({st.session_state.difficulty})")
        st.markdown(st.session_state.challenge)

        solution = get_solution()
        st.markdown("### AI Solution")
        st.write(solution)
    else:
        st.markdown(f"## Current Challenge ({st.session_state.difficulty})")
        st.markdown(st.session_state.challenge)

        # User code input
        user_code = st.text_area("Write your code here", height=200)

        if st.button("Submit Code") and not st.session_state.solution_revealed:
            feedback = get_feedback(user_code, st.session_state.challenge)
            st.session_state.feedback = feedback

            if "Good Job!" in feedback:
                points_awarded = {"Easy": 10, "Medium": 20, "Hard": 30}[st.session_state.difficulty]
                st.session_state.points += points_awarded
                st.success(f"Correct! You've been awarded {points_awarded} points.")
            else:
                st.error("Incorrect. Please try again.")

        # Display feedback
        if st.session_state.feedback:
            st.markdown("### AI Feedback")
            st.write(st.session_state.feedback)

        # Button to reveal the solution
        if st.button("Reveal Solution (Forfeit points)"):
            st.session_state.solution_revealed = True
            st.error("You will not be able to submit your solution once solutions have been revealed.")
            st.experimental_rerun()

# Points Display
st.markdown(f"## Your Points: {st.session_state.points}")

# Generate a new challenge
if st.button("Next Challenge"):
    st.session_state.difficulty = None
    st.session_state.challenge_type = None
    st.session_state.challenge = None
    st.session_state.feedback = ""
    st.session_state.solution_revealed = False
    st.experimental_rerun()
