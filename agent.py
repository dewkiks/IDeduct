from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
from langchain_together import ChatTogether
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
# llm = ChatTogether(
#          model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
#          together_api_key=os.getenv("TOGETHER_API_KEY")
#      )

class AgentState(TypedDict):
    case_details: AnyMessage
    discovered_info: str
    chat_history: str
    user_input: str
    router_info: str
    chat_history: list[str]

class Agent:
    def __init__(self, model):
        self.model = model
        self.graph = StateGraph(AgentState)

        self.graph.add_node("router",lambda state: state) #router node is created
        self.graph.add_node("mysterygen",RunnableLambda(self.mystery_generator))
        self.graph.add_node("suspect4",RunnableLambda(self.suspect4))
        self.graph.add_node("suspect3",RunnableLambda(self.suspect3))
        self.graph.add_node("suspect2",RunnableLambda(self.suspect2))
        self.graph.add_node("suspect1",RunnableLambda(self.suspect1))
        self.graph.add_node("default",RunnableLambda(self.default))
        self.graph.add_node("get_input",RunnableLambda(self.get_input))
        self.graph.add_node("solution",RunnableLambda(self.solution))

        self.graph.set_entry_point("mysterygen")
        self.graph.add_edge("mysterygen","get_input")

        while self.graph.add_conditional_edges("solution", self.solution) is True:
            self.graph.add_edge("get_input","router")
            self.graph.add_conditional_edges("router", self.router)
            self.graph.add_edge("suspect4","get_input")
            self.graph.add_edge("suspect3","get_input")
            self.graph.add_edge("suspect2","get_input")
            self.graph.add_edge("suspect1","get_input")
            self.graph.add_edge("default","get_input")

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
        state["case_details"] = result

        print(state["case_details"].content)

        instructions = """
        ===== Welcome to the Detective Mystery Game! =====
        Here are some commands you can use:
        - To interrogate a specific suspect, type:
            suspect 1
            suspect 2
            suspect 3
            suspect 4

            and then ask your question.
        - To ask the assistant for help, type: help
        - To check your current theory and the solution, type: solution check
        - If you need general assistance or hints, just ask your question.
        - To start a new mystery, type: generate mystery
        - To exit the game, type: exit or quit

        Let the investigation begin!
        ===============================================
        """
        print(instructions)

        return state 
    
    def get_input(self,state:AgentState):
        # Get user input and update state
        chat_history = state.get("chat_history", [])
        user_input = input("\nDetective: ")
        return {'user_input': user_input, 'chat_history': chat_history}
    
    def suspect4(self,state:AgentState):
        behaviour = state["case_details"].content
        chat_history = state.get("chat_history", [])
        prompt = f"""
        This is the details: {behaviour}
        analyse the details and find out what is the motive of the suspect 4.
        The suspect 4 is the one who is being questioned by the detective
        and you are suspect 4 in the case.

        this is the detective message/question: {state["user_input"]}

        You are a suspect in a detective mystery.
        You are being questioned by a detective.

        answer all the questions as if you are the suspect 4 in the case.
        only include the information that is relevant to the case.
        Do not include any information that is not relevant to the case. 
        """
        result = self.model.invoke(prompt)
        print(result.content)
        
        chat_history.append({"role": "detective", "content": state["user_input"]})
        chat_history.append({"role": "suspect 4", "content": result.content})
        state["chat_history"] = chat_history #update the chat history in the state
        return state #prompt being forwarded to model which is the LLM, then response stored in the result

    def suspect3(self, state: AgentState):
        behaviour = state["case_details"].content
        chat_history = state.get("chat_history", [])
        
        prompt = f"""
        This is the details: {behaviour}
        analyse the details and find out what is the motive of the suspect 3.
        The suspect 3 is the one who is being questioned by the detective
        and you are suspect 3 in the case.
        
        this is the detective message/question: {state["user_input"]}
        
        You are a suspect in a detective mystery.
        You are being questioned by a detective.
        
        answer all the questions as if you are the suspect 3 in the case.
        only include the information that is relevant to the case.
        Do not include any information that is not relevant to the case.
        """
        result = self.model.invoke(prompt)
        print(result.content)
        
        chat_history.append({"role": "detective", "content": state["user_input"]})
        chat_history.append({"role": "suspect 3", "content": result.content})
        state["chat_history"] = chat_history #update the chat history in the state
        return state    

    def suspect2(self, state: AgentState):
        behaviour = state["case_details"].content
        chat_history = state.get("chat_history", [])
        
        prompt = f"""
        This is the details: {behaviour}
        analyse the details and find out what is the motive of the suspect 2.
        The suspect 2 is the one who is being questioned by the detective
        and you are suspect 2 in the case.
        
        this is the detective message/question: {state["user_input"]}
        
        You are a suspect in a detective mystery.
        You are being questioned by a detective.
        
        answer all the questions as if you are the suspect 2 in the case.
        only include the information that is relevant to the case.
        Do not include any information that is not relevant to the case.
        """
        result = self.model.invoke(prompt)
        print(result.content)
        
        chat_history.append({"role": "detective", "content": state["user_input"]})
        chat_history.append({"role": "suspect 2", "content": result.content})
        state["chat_history"] = chat_history #update the chat history in the state
        return state

    def suspect1(self, state: AgentState):
        behaviour = state["case_details"].content
        chat_history = state.get("chat_history", [])
        
        prompt = f"""
        This is the details: {behaviour}
        analyse the details and find out what is the motive of the suspect 1.
        The suspect 1 is the one who is being questioned by the detective
        and you are suspect 1 in the case.
        
        this is the detective message/question: {state["user_input"]}
        
        You are a suspect in a detective mystery.
        You are being questioned by a detective.
        
        answer all the questions as if you are the suspect 1 in the case.
        only include the information that is relevant to the case.
        Do not include any information that is not relevant to the case.
        """
        result = self.model.invoke(prompt)
        print(result.content)
        
        chat_history.append({"role": "detective", "content": state["user_input"]})
        chat_history.append({"role": "suspect 1", "content": result.content})
        state["chat_history"] = chat_history #update the chat history in the state
        return state
    
    def default(self, state: AgentState):
        behaviour = state["case_details"].content
        chat_history = state.get("chat_history", [])
        detective_input = state["user_input"]
        
        prompt = f"""
        You are an assistant detective helping with a case investigation.
        
        CASE DETAILS: {behaviour}
        
        DETECTIVE'S CURRENT REQUEST: "{detective_input}"
        
        CONVERSATION HISTORY: {chat_history}
        
        As the detective's assistant:
        1. Analyze the detective's request and provide guidance
        2. If they request information or analysis, provide it based on the case details
        3. If they seem lost or unsure, suggest next steps in the investigation
        4. Occasionally offer subtle hints or observations that might help solve the case
        5. If they ask for a summary of findings so far, provide it based on the chat history
        6. Always remain objective and professional
        
        Remember:
        - Don't reveal the solution outright
        - Don't make up information not present in the case details
        - Maintain the mystery and challenge of the investigation
        - Encourage the detective to question all suspects thoroughly
        
        Respond in a helpful, analytical tone suitable for a detective's assistant.
        """
        
        result = self.model.invoke(prompt)
        print(result.content)
        
        chat_history.append({"role": "detective", "content": detective_input})
        chat_history.append({"role": "assistant", "content": result.content})
        state["chat_history"] = chat_history
        
        return state

    
    def solution(self, state: AgentState):
        behaviour = state["case_details"].content
        chat_history = state.get("chat_history", [])
        user_input = state["user_input"].lower()
        
        # Create a comprehensive analysis prompt
        prompt = f"""
        You are a master detective analyzing a case.
        
        CASE DETAILS: {behaviour}
        
        INVESTIGATION RECORDS: {chat_history}
        
        DETECTIVE'S REQUEST: "{user_input}"
        
        Based on all available evidence and interrogations, provide:
        1. A summary of the key facts discovered
        2. Analysis of each suspect's motives, alibis, and evidence against them
        3. Your conclusion about who the culprit is and why
        4. Any remaining loose ends or unanswered questions
        
        If there isn't sufficient evidence to solve the case:
        - Identify what crucial information is still missing
        - Suggest specific questions the detective should ask next
        - Note which suspects need further interrogation
        
        FORMAT YOUR RESPONSE:
        - Begin with "CASE SOLVED" or "CASE INCOMPLETE" on its own line
        - Then provide your full analysis in a clear, logical manner
        - Be definitive in your conclusion if the case is solved
        - Be specific about next steps if the case is incomplete
        """
        
        result = self.model.invoke(prompt)
        print("\n===== DETECTIVE'S ANALYSIS =====")
        print(result.content)
        print("================================\n")
        
        chat_history.append({"role": "detective", "content": user_input})
        chat_history.append({"role": "analysis", "content": result.content})
        state["chat_history"] = chat_history
        
        if "CASE SOLVED" in result.content:
            follow_up = input("\nCase solved! Type 'end' to conclude or anything else to continue: ")
            if follow_up.lower().strip() == "end":
                print("\n===== CASE CLOSED =====\n")
                return END
        
        return "get_input"
    
    def router(self,state:AgentState):
        user_input = state["user_input"].lower()
        chat_history = state.get("chat_history", [])
        prompt = f"""
            Given the detective mystery context, determine which handler should process the current user message.

            DETECTIVE'S CURRENT MESSAGE: "{user_input}"

            CONVERSATION CONTEXT:
            - Mystery details previously established:
            - Chat history: {chat_history}

            ROUTING INSTRUCTIONS:
            1. If the user explicitly wants to speak with a specific suspect:
            - "suspect 4" or "fourth suspect" -> return EXACTLY "suspect4"
            - "suspect 3" or "third suspect" -> return EXACTLY "suspect3" 
            - "suspect 2" or "second suspect" -> return EXACTLY "suspect2"
            - "suspect 1" or "first suspect" -> return EXACTLY "suspect1"
            - "solution check" or "check solution" -> return EXACTLY "solution"
            - "exit" or "quit" -> return EXACTLY "exit"

            2. If no specific suspect is mentioned but the detective is CONTINUING an interrogation:
            - If the last conversation was with suspect 4 -> return "suspect4"
            - If the last conversation was with suspect 3 -> return "suspect3"
            - If the last conversation was with suspect 2 -> return "suspect2" 
            - If the last conversation was with suspect 1 -> return "suspect1"


            3. If the user wants a new case/mystery -> return EXACTLY "mysterygen"

            4. For any other query or help -> return EXACTLY "default"

            OUTPUT FORMAT: Return ONLY the destination string (e.g., "suspect4") with no additional text.
            """

        result = self.model.invoke(prompt)
        result = result.content.lower()

        if "generate mystery" in result:
            return "mysterygen"
        elif "suspect4" in result:
            return "suspect4"
        elif "suspect3" in result:
            return "suspect3"
        elif "suspect2" in result:
            return "suspect2"
        elif "suspect1" in result:
            return "suspect1"
        elif "solution check" in result:
            return "solution"
        elif "exit" or "quit" in result:
            return END
        else:
            return "default"

def main():    
        agent = Agent(llm)
        agent.graph.invoke({})        
main()