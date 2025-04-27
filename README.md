# 🕵️‍♂️ Detective Mystery Game

**Welcome to the Detective Mystery Game!**  
Step into the shoes of a detective solving thrilling mysteries inspired by Sherlock Holmes and Agatha Christie.  
Powered by **Streamlit**, **LangGraph**, and **LangChain**, it generates unique cases with AI-crafted suspect portraits and crime scene visuals.  
Interrogate suspects, analyze clues, and crack the case!

---

## 📑 Table of Contents
- Features
- Technologies
- Installation
- Usage
- Game Commands
- File Structure
- Environment Variables
- Contributing
- License

---

## ✨ Features
- **Dynamic Mystery Generation**: Unique crime stories with four suspects having motives, access, and evidence.
- **Interactive Suspect Interrogation**: AI-generated suspect responses tailored to each case.
- **AI-Generated Visuals**: Suspect portraits and crime scenes using Pollinations AI and Gemini.
- **Emotion Analysis**: Suspect emotions update dynamically based on your questions.
- **Streamlit Interface**: Sleek UI with chat history, case briefings, and debug tools.
- **LangGraph Workflow**: Smart routing of player inputs to correct game handlers.
- **Case Analysis**: Detailed breakdowns after solution checks.

---

## 🛠️ Technologies
- Python 3.8+
- Streamlit
- LangChain (Google Gemini, Together AI)
- LangGraph
- Pillow (PIL)
- Requests
- Google Generative AI
- Dotenv

---

## 📥 Installation

**Clone the Repository**:
```bash
git clone https://github.com/your-username/detective-mystery-game.git
cd detective-mystery-game
```

**Install Dependencies**:
```bash
pip install -r requirements.txt
```
Sample `requirements.txt`:
```
streamlit
langchain
langchain-google-genai
langchain-together
python-dotenv
pillow
requests
google-generativeai
```

**Set Up Environment Variables**:
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key
TOGETHER_API_KEY=your_together_api_key
```

**Run the Application**:
```bash
streamlit run main.py
```
Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🎮 Usage
- **Start a New Case**: Click "Start New Case" to generate a mystery.
- **Interrogate Suspects**: Use the chat input to question suspects (e.g., `suspect 1`) or check your solution.
- **View Visuals**: See suspect portraits and crime scene images.
- **Analyze the Case**: Use `solution check` for case breakdowns.
- **Debugging**: Sidebar shows logs and suspect emotion states.

---

## 🗣️ Game Commands
- `suspect 1`, `suspect 2`, `suspect 3`, `suspect 4`: Interrogate a suspect.
- `solution check`: Validate your investigation.
- `help`: Request hints.
- `generate mystery`: Start a new case.
- `exit` or `quit`: End the current case.

---

## 📂 File Structure
```
detective-mystery-game/
├── main.py                # Main Streamlit app and game logic
├── agent.py               # LangGraph agent for state management
├── detective_engine.py    # Image generation and emotion analysis
├── .env                   # API keys
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── gemini-native-image.png # Temporary crime scene image
```

---

## 🔑 Environment Variables
Set these in your `.env` file:
- `GEMINI_API_KEY`: For Google Gemini.
- `TOGETHER_API_KEY`: For Together AI.

Get your API keys from:
- [Google Cloud Console](https://console.cloud.google.com/)
- [Together AI](https://www.together.ai/)

---

## 🤝 Contributing
We welcome contributions!  
To contribute:
1. Fork the repo.
2. Create a feature branch.
3. Commit your changes.
4. Push and open a pull request.

Please follow PEP 8 standards and include tests if possible.

---

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

---

Made with ❤️ by dewkiks
