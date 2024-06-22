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
  <li>Code debugging tools to identify and resolve errors</li>
  <li>Progress tracking and point system to motivate learning</li>
</ul>

## Installation and Usage

1. Clone the repository:

```bash
git clone https://github.com/brayden-sim/CloudHacks24-.git
```

2. Install Dependencies
```bash
pip install streamlit google.generativeai
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
