import streamlit as st
import google.generativeai as genai

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

# Function to generate a coding challenge
def generate_challenge(difficulty):
    difficulty_map = {
        'Easy': 'an easy',
        'Medium': 'a medium',
        'Hard': 'a hard'
    }
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(f"Generate {difficulty_map[difficulty]} coding challenge for beginners in Python. Include only the description, sample input, and sample output. Do not generate any solutions. Give hints such as what functions or methods to use.")
    return response.text.strip()

# Function to get AI feedback
def get_feedback(code):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(f"Evaluate the correctness of this Python code:\n{code}")
    return response.text.strip()

# Function to get AI solution
def get_solution():
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(f"Generate the solution for this coding challenge:\n{st.session_state.challenge}")
    return response.text.strip()

# Initialize session state
if 'points' not in st.session_state:
    st.session_state.points = 0

if 'difficulty' not in st.session_state:
    st.session_state.difficulty = None

if 'challenge' not in st.session_state:
    st.session_state.challenge = None

if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

if 'solution_revealed' not in st.session_state:
    st.session_state.solution_revealed = False

# Difficulty selection
st.title("AI-Powered Python Challenge")
difficulty = st.selectbox("Select difficulty", ['Easy', 'Medium', 'Hard'])

if st.button("Generate Challenge"):
    st.session_state.difficulty = difficulty
    st.session_state.challenge = generate_challenge(difficulty)
    st.session_state.feedback = ""
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
            feedback = get_feedback(user_code)
            st.session_state.feedback = feedback

            if "correct" in feedback.lower() or "acceptable" in feedback.lower():
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
        if st.button("Reveal Solution"):
            st.session_state.solution_revealed = True
            st.experimental_rerun()

# Points Display
st.markdown(f"## Your Points: {st.session_state.points}")

# Generate a new challenge
if st.button("Next Challenge"):
    st.session_state.difficulty = None
    st.session_state.challenge = None
    st.session_state.feedback = ""
    st.session_state.solution_revealed = False
    st.experimental_rerun()
