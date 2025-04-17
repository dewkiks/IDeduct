from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()
import os

llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-001",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY")
        )

class AgentState(TypedDict):
    case_details: AnyMessage
    discovered_info: str
    chat_history: str
    user_input: str

class Agent:
    def __init__(self, model):
        self.model = model
        self.graph = StateGraph(AgentState)
        self.graph.set_entry_point("mysterygen")
        self.graph.add_node("mysterygen",self.mystery_generator)
        self.graph.add_edge("mysterygen",END)
        
        self.graph = self.graph.compile()
    
    def mystery_generator(self,state:AgentState):
        prompt = ([HumanMessage("""
        Create a detective mystery with multiple possible culprits.
    
        Generate:
        1. A crime description
        2. 3-4 suspects with these details for each:
        - Name and role
        - Strong motive for the crime
        - Access to crime scene
        - One suspicious fact
        - One piece of evidence pointing to them
        
        Make sure multiple suspects could reasonably be guilty based on the evidence.
        Format your response as a case briefing to a detective.""")])
        result = self.model.invoke(prompt) #prompt being forwarded to model which is the LLM, then response stored in the result
        state["case_details"] = result #result response is then stored to the state
        return state #state values are returned
    
def main():
        
        agent = Agent(llm) 

        result = agent.graph.invoke({"case_details": ""})

        # Print the result
        print(result["case_details"])

main()