import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import google.generativeai as genai
import yaml
import os
import json
import random
import time
import base64
from streamlit_navigation_bar import st_navbar
from streamlit_lottie import st_lottie
import pandas as pd
import matplotlib.pyplot as plt


#st.set_page_config(layout="wide")
#login


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
#css
styles = {
    "nav": {
        "background-color": "dark grey",
        "justify-content": "left",
        "border-radius": "5px",
        "-moz-box-shadow": "1px 2px 3px rgba(0,0,0,.5)",
        "-webkit-box-shadow": "1px 2px 3px rgba(0,0,0,.5)",
        "box-shadow": "1px 2px 3px rgba(0,0,0,.5)",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
               
        "color": "white",
        "padding": "14px",
        "font-family": "Helvetica",
        "font-size": "25",
    },
    "active": {
        "background-color": "black",
        "border-radius": "5px",
        "-moz-box-shadow": "1px 2px 3px rgba(0,0,0,.5)",
        "-webkit-box-shadow": "1px 2px 3px rgba(0,0,0,.5)",
        "box-shadow": "1px 2px 3px rgba(0,0,0,.5)",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
        "font-family": "Helvetica"
    }
}

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://coolbackgrounds.io/images/backgrounds/index/compute-ea4c57a4.png");
    background-position: center;  
    background-repeat: no-repeat;
    object-fit: cover
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Source+Code+Pro:ital,wght@0,200..900;1,200..900&display=swap');        
    h1 {
      font-size: 60px;
      font-weight: 700
      text-align: left;
      text-transform: uppercase;
      font-family: "Montserrat" 
   }
   div.element-container st-emotion-cache-ifpscm e1f1d6gn4 {
      left: 200px      
    }
</style>
""", unsafe_allow_html=True)

#load animations
def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
lottie_congrats = load_lottiefile("congrats.json");   

# File to store generated challenges
GENERATED_CHALLENGES_FILE = 'generated_challenges.json'
PROGRESS_FILE = 'progress.json'


# Load generated challenges
if os.path.exists(GENERATED_CHALLENGES_FILE):
    try:
        with open(GENERATED_CHALLENGES_FILE, 'r') as file:
            generated_challenges = json.load(file)
    except json.JSONDecodeError:
        generated_challenges = []
else:
    generated_challenges = []

# Function to record challenge completion
def record_challenge_completion(challenge_type, difficulty, time_taken):
    progress_data = {
        "challenge_type": challenge_type,
        "difficulty": difficulty,
        "time_taken": time_taken,
        "timestamp": time.time()
    }
    
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            progress = json.load(f)
    else:
        progress = []
    
    progress.append(progress_data)
    
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f)

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

    # Generate a new challenge
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(
        f"Generate {difficulty_map[difficulty]} coding challenge for beginners in Python {type_map[challenge_type]}. "
        f"Include only the description, sample input, and sample output. Do not generate any solutions. "
        f"Give hints such as what functions or methods to use."
        f"Do not use repeat any challenges found in {generated_challenges}"
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

#NAVIGATION BAR
page = st_navbar(["Home", "Leaderboard", "About", "Progress"],styles=styles)
st.write(page)

if page == "Home":

    #header
    st.title("OVERCODE.")
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
                    congrats_placeholder = st.empty()
                    with congrats_placeholder:
                        st_lottie(lottie_congrats, speed=0.75, quality="high", height=200, width=200 )
                    time.sleep(1.5)
                    congrats_placeholder.empty()

                else:
                    st.error("Incorrect. Please try again.")
                st.session_state.solution_revealed = True

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

    # Predefined list of jokes
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None. It's a hardware problem.",
        "Why do Java developers wear glasses? Because they don't C#.",
        "Why do programmers hate nature? It has too many bugs.",
        "Why did the programmer go broke? Because he used up all his cache.",
        "What is a programmer's favorite snack? Computer chips.",
        "Why did the programmer quit his job? Because he didn't get arrays.",
        "What's a pirate's favorite programming language? R!",
    ]

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

    # Joke of the Day (optional fun feature)
    st.header("")
    st.write("Feeling tired? Check out some jokes!")
    if st.button("Tell me a joke"):
        joke = random.choice(jokes)
        st.write(joke)

        components.html(f"""
        {tts_script}
        <button onclick="speakElement('joke-text')">👂 Read Joke!</button>
        <p id="joke-text" style="display:none">{joke}</p>
        """, height=60)
        
elif page == "Progress":
    st.title("Progress")
    
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            progress = json.load(f)
        
        if progress:
            df = pd.DataFrame(progress)
            st.write("### Challenge Completion Stats")
            st.write(df)
            
            # Pie chart of challenge types
            challenge_counts = df['challenge_type'].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(challenge_counts, labels=challenge_counts.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.write("#### Distribution of Challenge Types")
            st.pyplot(fig1)
            
            # Bar chart of difficulty levels
            difficulty_counts = df['difficulty'].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.bar(difficulty_counts.index, difficulty_counts)
            ax2.set_xlabel("Difficulty Level")
            ax2.set_ylabel("Number of Challenges")
            st.write("#### Challenges by Difficulty Level")
            st.pyplot(fig2)
            
            # Histogram of time taken
            fig3, ax3 = plt.subplots()
            ax3.hist(df['time_taken'], bins=10)
            ax3.set_xlabel("Time Taken (seconds)")
            ax3.set_ylabel("Number of Challenges")
            st.write("#### Time Taken for Challenges")
            st.pyplot(fig3)
        else:
            st.write("No progress data available.")
    else:
        st.write("No progress data available.")
elif page == "About":
    st.title("About")
    st.write("Overcoding is a streamlined platform built on Streamlit, designed for users to enhance their coding skills effectively. Whether you're a novice or an experienced programmer, Overcoding offers tailored learning modules in Easy, Medium, and Hard difficulty levels")