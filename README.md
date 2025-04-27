Detective Mystery Game 🕵️‍♂️
Welcome to the Detective Mystery Game, an interactive web app where you solve thrilling mysteries inspired by Sherlock Holmes and Agatha Christie. Built with Streamlit, LangGraph, and LangChain, it generates dynamic cases with AI-crafted suspect portraits and crime scenes. Interrogate suspects, analyze clues, and crack the case! 🔍
Table of Contents

Features
Technologies
Installation
Usage
Game Commands
File Structure
Environment Variables
Contributing
License

Features

Dynamic Mystery Generation: Unique crime stories with four suspects, including motives, access, and evidence.
Interactive Suspect Interrogation: Question suspects with AI-generated responses.
AI-Generated Visuals: Suspect portraits and crime scenes via Pollinations AI and Gemini.
Emotion Analysis: Suspects’ emotions (e.g., nervous, guilty) update based on questions.
Streamlit Interface: User-friendly UI with chat history, case briefings, and debug tools.
LangGraph Workflow: State machine for routing player inputs.
Case Analysis: Detailed solution analysis with next steps.

Technologies

Python 3.8+
Streamlit: Web interface.
LangChain: AI model integration (Google Gemini, Together AI).
LangGraph: Game state management.
Pillow (PIL): Image processing.
Requests: Fetches AI-generated images.
Google Generative AI: Text and image generation.
Dotenv: API key management.

Installation

Clone the Repository:
git clone https://github.com/your-username/detective-mystery-game.git
cd detective-mystery-game


Install Dependencies:Ensure Python 3.8+. Install packages:
pip install -r requirements.txt

Sample requirements.txt:
streamlit
langchain
langchain-google-genai
langchain-together
python-dotenv
pillow
requests
google-generativeai


Set Up Environment Variables:Create a .env file:
GEMINI_API_KEY=your_gemini_api_key
TOGETHER_API_KEY=your_together_api_key


Run the Application:Start the app:
streamlit run main.py

Open http://localhost:8501 in your browser.


Usage

Start a New Case: Click "Start New Case" to generate a mystery.
Interrogate Suspects: Use chat input to question suspects (e.g., suspect 1) or check solutions (solution check).
View Visuals: Suspect portraits and crime scenes update with emotions.
Analyze the Case: Use solution check for case analysis.
Debugging: Sidebar shows debug log and suspect emotions.

Game Commands

suspect 1, suspect 2, suspect 3, suspect 4: Interrogate a suspect.
solution check: Check your solution.
help: Get hints.
generate mystery: Start a new case.
exit or quit: End the case.

File Structure
detective-mystery-game/
├── main.py                # Main app and game logic
├── agent.py               # LangGraph agent
├── detective_engine.py    # Image generation and emotion analysis
├── .env                   # API keys
├── requirements.txt       # Dependencies
├── README.md              # This file
└── gemini-native-image.png # Temporary crime scene image

Environment Variables
Add to .env:

GEMINI_API_KEY: Google Gemini API key.
TOGETHER_API_KEY: Together AI key.

Get keys from:

Google Cloud Console for Gemini.
Together AI for Llama models.

Contributing
To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

Follow PEP 8 and include tests.
License
This project is licensed under the MIT License. See the LICENSE file.

🕵️‍♂️ Solve the mystery and uncover the truth! 🔍
