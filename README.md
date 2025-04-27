# LangGraph Detective Mystery Game

This Python code implements an interactive detective mystery game using LangGraph, Langchain, and a Large Language Model (LLM) like Gemini or Llama 3. You, the user, take on the role of a detective investigating a crime, interrogating suspects, and ultimately trying to solve the mystery.

## Features

* **Dynamic Mystery Generation:** Each time you start the game, a new and unique detective mystery is generated, complete with a crime description, multiple suspects, motives, clues, and suspicious facts.
* **Interactive Interrogation:** You can directly question each of the suspects by typing commands like "suspect 1" followed by your question. The LLM will roleplay as the suspect, providing answers based on the initial case briefing.
* **Detective Assistant:** An in-game assistant is available to provide guidance, analyze the case, offer hints, and summarize findings as you progress. Just ask your questions or for help.
* **Solution Checking:** You can present your theory and ask for a solution check. The LLM will analyze the evidence and your investigation history to determine if the case is solved and provide a conclusion.
* **State Management with LangGraph:** The game's flow and information are managed using LangGraph's `StateGraph`, ensuring a structured and coherent investigation process.
* **Flexibility with LLMs:** The code is set up to use either Google's Gemini model (via `ChatGoogleGenerativeAI`) or Together AI's Llama 3 model (via `ChatTogether`), allowing you to choose your preferred LLM by uncommenting the relevant section and ensuring the corresponding API key is set in your `.env` file.
* **Clear Command Interface:** Simple text-based commands allow for easy interaction with the game.

## Setup

### Prerequisites

* **Python 3.7+**
* **pip** (Python package installer)
* An API key for either Google Gemini or Together AI.

### Installation

1.  **Clone the repository** (if you have the code in a repository). If you have the Python file directly, skip this step.
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install langchain langchain-google-genai python-dotenv typing-extensions langchain-together
    ```

3.  **Create a `.env` file:** In the same directory as your Python script, create a file named `.env`.

4.  **Add your API key(s) to the `.env` file:**
    * **For Google Gemini:**
        ```dotenv
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        ```
        Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key. You can obtain one from the [Google AI Studio](https://makersuite.google.com/).

    * **For Together AI (Llama 3):**
        ```dotenv
        TOGETHER_API_KEY=YOUR_TOGETHER_API_KEY
        ```
        Replace `YOUR_TOGETHER_API_KEY` with your actual Together AI API key. You can obtain one from the [Together AI platform](https://www.together.ai/).

    * **Note:** You only need to add the API key for the LLM you intend to use. The code currently defaults to Gemini, but you can switch to Llama 3 by commenting/uncommenting the `llm` instantiation lines.

## How to Play

1.  **Run the Python script:**
    ```bash
    python your_script_name.py
    ```
    Replace `your_script_name.py` with the actual name of the Python file.

2.  **The game will start by generating a new mystery and providing a case briefing.** The details of the crime and the suspects will be printed to the console.

3.  **Follow the on-screen instructions to interact with the game:**
    * **Interrogate suspects:** Type `suspect 1`, `suspect 2`, `suspect 3`, or `suspect 4` followed by your question.
    * **Ask for help:** Type your question directly.
    * **Check your theory:** Type `solution check`.
    * **Start a new mystery:** Type `generate mystery`.
    * **Exit the game:** Type `exit` or `quit`.

4.  **Continue to investigate by questioning suspects and using the assistant until you believe you have solved the case.**

## Code Explanation

* **Import necessary libraries:** Imports modules from `langgraph`, `langchain_core`, `langchain_google_genai`, `langchain_together`, `dotenv`, and `typing`.
* **Load environment variables:** Loads API keys from the `.env` file.
* **Initialize LLM:** Sets up either the `ChatGoogleGenerativeAI` or `ChatTogether` model with specified parameters.
* **`AgentState`:** A `TypedDict` defining the structure of the state that will be passed between nodes in the LangGraph.
* **`Agent` Class:**
    * **`__init__(self, model)`:** Initializes the agent with the provided LLM and sets up the LangGraph. It defines the nodes for different actions (router, mystery generation, suspect interrogation, default handling, solution checking, and input gathering) and the edges connecting them, including conditional edges for the router and the solution.
    * **`mystery_generator(self, state: AgentState)`:** Generates a new detective mystery and prints the case briefing and instructions to the console. It updates the `case_details` in the LangGraph state.
    * **`get_input(self, state: AgentState)`:** Prompts the user for input and updates the `user_input` and `chat_history` in the state.
    * **`suspect1` to `suspect4(self, state: AgentState)`:** These methods handle the interrogation of each specific suspect. They formulate a prompt that includes the case details, the detective's question, and the role-playing instruction for the LLM to act as the respective suspect. The suspect's response is printed, and the chat history is updated.
    * **`default(self, state: AgentState)`:** Handles general questions or requests for help from the detective. It prompts the LLM to act as an assistant detective, providing guidance based on the case details and conversation history.
    * **`solution(self, state: AgentState)`:** Handles the detective's request to check the solution. It prompts the LLM to analyze the case details and investigation records to provide a summary, suspect analysis, a conclusion (if possible), and any remaining questions. It also handles the end-game scenario if the case is solved.
    * **`router(self, state: AgentState)`:** This crucial method determines the next node in the LangGraph based on the user's input. It uses the LLM to classify the input and decide whether to interrogate a specific suspect, check the solution, start a new mystery, or use the default assistant.
* **`main()`:** Creates an instance of the `Agent` class and invokes the LangGraph to start the game.

## Contributions

Contributions to this project are welcome! Feel free to fork the repository, make improvements, and submit pull requests. You can contribute by:

* Adding new features or game mechanics.
* Improving the prompts for better LLM responses.
* Adding more sophisticated routing logic.
* Implementing error handling and input validation.
* Writing more comprehensive documentation.

## License

This project is licensed under the [Specify License Here] License.

