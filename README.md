# CloudHacks24
<p>This is a collborative project for the CloudHacks2024 Hackathon.</p>

## Description
Overcoding is a streamlined platform built on Streamlit, designed for users to enhance their coding skills effectively. Whether you're a novice or an experienced programmer, Overcoding offers tailored learning modules in Easy, Medium, and Hard difficulty levels.</br>
With AI-powered feedback, Overcoding evaluates your code submissions instantly, providing insightful critiques and suggestions for improvement. This interactive feature ensures that you receive personalized guidance to refine your coding techniques and tackle challenges with confidence.</br></br>
Start mastering coding fundamentals and advancing your skills in a supportive learning environment!</br>
Empower yourself to write better code and achieve your programming goals with CodeMentor's intuitive platform. Take the next step in your coding journey today.

## Features
<ul>
  <li>Interactive coding exercises with real-time feedback</li>
  <li>AI-generated assessments to evaluate code quality and efficiency</li>
  <li>Jokes to make your day! (with built-in TTS function)</li>
  <li>Progress tracking and point system to motivate learning</li>
</ul>

## How we built it
Overcode was developed using Streamlit for its interactive and user-friendly interface. Key components include:

Frontend: Streamlit for real-time rendering of coding exercises and feedback.
Backend: Python integrated with AI models to assess and provide feedback on code quality.
Libraries and Tools:
<ul>
  <li>streamlit for the application framework.</li>
  <li>google.generativeai for AI feedback.</li>
  <li>streamlit-navigation-bar for easy navigation.</li>
  <li>streamlit-lottie for animations.</li>
  <li>streamlit-authenticator for user authentication.</li>
</ul>

## Challenges we ran into
<ul>
  <li>Real-Time Feedback Accuracy: Ensuring that AI-generated feedback is both accurate and useful.</li>
  <li>Challenge Duplication: Generating unique challenges each time to avoid repetition.</li>
  <li>Point System Integrity: Preventing users from exploiting the points system by repeatedly submitting the same solution.</li>
  <li>User Experience: Balancing the complexity of the interface with ease of use, especially for beginners.</li>
</ul>

## Accomplishments that we're proud of
<ul>
  <li>Seamless AI Integration: Successfully implementing AI that provides insightful and actionable feedback.</li>
  <li>Dynamic Learning Paths: Creating a system that adjusts difficulty based on user performance.</li>
  <li>Robust Progress Tracking: Developing a motivational points and badge system that accurately reflects user achievements.</li>
</ul>

## What we learned
<ul>
<li>Effective AI Utilization: Gained insights into integrating AI for educational feedback purposes.</li>
<li>Streamlit Capabilities: Explored the extensive functionalities of Streamlit for creating interactive web applications.</li>
</ul>

## Installation and Usage

1. Clone the repository:

```bash
git clone https://github.com/brayden-sim/CloudHacks24-.git
```

2. Install Dependencies
```bash
pip install streamlit google.generativeai
pip install streamlit
pip install streamlit-navigation-bar
pip install streamlit-lottie
pip install streamlit-authenticator
```
or
```bash
pip install -r requirements.txt
```
3. Run the script
   
```bash
python -m streamlit run .\sample.py
```
or
```bash
streamlit run .\sample.py
```
TO FIX:
- When generating a challenge of the same difficulty and type, the same challenge will be generated
- The user can press the "Submit code" button multiple times to receive points more than once
- "Reveal Solution" button is still there after the user has completed the challenge correctly
