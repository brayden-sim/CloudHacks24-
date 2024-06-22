import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import random
import csv

# Configure the Gemini API
genai.configure(api_key="AIzaSyAZ7myOXP5C5GS4wOq5X4yTstZ2ttH5eos")

# Text to Speech TTS JavaScript Function
tts_script = """
<script>
    function speakText(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }

    function speakElement(id) {
        const element = document.getElementById(id);
        if (element) {
            speakText(element.innerText || element.textContent);
        }
    }
</script>
"""

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

# Initialize session state
if 'points' not in st.session_state:
    st.session_state.points = 0

if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'Easy'

if 'challenge' not in st.session_state:
    st.session_state.challenge = generate_challenge(st.session_state.difficulty)

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
    # Simple check for demo purposes (customize for real use)
    if "def" in code_input and "return" in code_input:
        st.success("Challenge attempt submitted! You've earned 10 points.")
        st.session_state.points += 10
    else:
        st.error("Submission doesn't meet the challenge requirements. Try again.")

    # Get AI feedback
    feedback = get_feedback(code_input)
    st.markdown("### AI Feedback")
    st.write(feedback)


# Function to insert feedback into a CSV file
def insert_feedback_to_csv(rating, feedback):
    with open('feedback.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([rating, feedback])

# UI for feedback
st.markdown("### Rate this Challenge")
rating = st.slider("Rating", min_value=1, max_value=5, value=3)
feedback = st.text_area("Feedback")

# Button to submit feedback
if st.button("Submit Feedback"):
    if rating and feedback:
        insert_feedback_to_csv(rating, feedback)
        st.success("Thank you for your feedback! It has been saved.")
    else:
        st.error("Please provide both a rating and feedback.")

# Button to view feedback
if st.button("View Feedback"):
    with open('feedback.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        feedback_data = list(reader)
    for row in feedback_data:
        st.write(f"Rating: {row[0]}")
        st.write(f"Feedback: {row[1]}")
        st.write("---")

# Points Display
st.markdown(f"## Your Points: {st.session_state.points}")

# Generate a new challenge
if st.button("Skip Challenge"):
    st.session_state.challenge = generate_challenge(st.session_state.difficulty)

# Joke of the Day (optional fun feature)
if st.button("Tell me a joke"):
    joke = random.choice(jokes)
    st.write(joke)

    components.html(f"""
    {tts_script}
    <button onclick="speakElement('joke-text')">🔊 Read Joke</button>
    <p id="joke-text" style="display:none">{joke}</p>
    """, height=60)
