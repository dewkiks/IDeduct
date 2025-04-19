from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables.router import RouterRunnable
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

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
    get_input : str
    discovered_info: str
    chat_history: str
    user_input: str
    router_info: str

class Agent:
    def __init__(self, model):
        self.model = model
        self.graph = StateGraph(AgentState)

        self.graph.set_entry_point("mysterygen")
        self.graph.add_node("router",lambda state: state) #router node is created
        self.graph.add_node("mysterygen",RunnableLambda(self.mystery_generator))
        self.graph.add_node("suspect4",RunnableLambda(self.suspect4))
        self.graph.add_node("suspect3",RunnableLambda(self.suspect3))

        self.graph.add_edge("mysterygen","router")
        self.graph.add_conditional_edges("router", self.router)
        self.graph.add_edge("router",END)

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
        
        you can grab inspiration from sherlock holmes, agatha christie, or any other detective story.
        Make sure multiple suspects could reasonably be guilty based on the evidence.
        Format your response as a case briefing to a detective.
        """)])
        result = self.model.invoke(prompt) #prompt being forwarded to model which is the LLM, then response stored in the result
        state["case_details"] = result #result response is then stored to the state
        # print(state["case_details"].content) #print the case details
        return state #state values are returned
    
    def suspect4(self,state:AgentState):
        print("i am suspect 4")
    
    def suspect3(self,state:AgentState):
        print("i am suspect 3")

    def router(self,state:AgentState):
        print(state["case_details"].content) #print the case details
        previous_message = state["case_details"].content
        user_input = state["user_input"].lower()
        prompt = PromptTemplate(
        input_variables=["previous_message", "user_message"],
        template="""
        This is the previous message: {previous_message}

        This is the user message: {user_message}
        Based on the previous message and user message, determine the next step.
        
        see what the user is asking for and return like this:
        - if the user is asking to question suspect 4 and suspect 4 only, return "suspect4"
        - if the user is asking to question suspect 3 and suspect 3 only, return "suspect3"
        - if the user is asking to generate a mystery, return "mysterygen"

        only return the value i above said inside the " " double quotes and nothing else.
        Do not add any additional comments or explanations.
        """
        )
        #TEXT SUMMARIZATION
        llm_chain = prompt | self.model | StrOutputParser() #llm_chain is the chain of LLMs and prompts
        text_summaries=llm_chain.invoke({"previous_message": previous_message, "user_message": user_input}) #invoke the llm_chain with the previous message and user input
        state["router_info"] = text_summaries #text summaries are stored in the state
        #print(text_summaries) #print the text summaries
        result = text_summaries #result is the content of the text summaries

        if "generate mystery" in result:
            return state, "mysterygen"
        elif "suspect 4" in result:
            return state, "suspect4"
        else:
            return state, "suspect3"

def main():
        
        
        agent = Agent(llm)
        user_input = input("What do you want to do? (e.g., 'generate mystery' or 'suspect 4')\n> ")

    # Run graph
        agent.graph.invoke({
            "user_input": user_input,
            "case_details": ""  # initially empty
        })
        
main()