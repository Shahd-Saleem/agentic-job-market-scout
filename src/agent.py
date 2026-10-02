import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools import search_jobs, analyze_skill_gaps

# Load environment variables from .env
load_dotenv()

def run_talent_scout():
    print("Initializing TalentScout AI Agent...")
    
    # Ensure API key exists
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in your environment variables. Make sure your .env file is set up.")
        return
        
    # Initialize Gemini Model
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Register Tools & Bind to Model
    tools = [search_jobs, analyze_skill_gaps]
    llm_with_tools = llm.bind_tools(tools)
    
    # Define the System Persona & Interactive Conversational Flow
    system_prompt = SystemMessage(content="""
    You are TalentScout AI, an elite career advisor and technical recruiter specialized in the UAE tech market (Dubai/Riyadh) and top-tier global firms.
    
    YOUR INTERACTIVE WORKFLOW:
    1. Warmly greet the candidate and introduce your purpose (helping them evaluate career fit and skill gaps).
    2. Conversational Discovery: Proactively ask the user for their details step-by-step if they haven't provided them yet:
       - Industry / Field (e.g., AI Engineering, Software Engineering, Cybersecurity, Consulting, Product Management, etc.)
       - Seniority / Role Level (e.g., Intern, Junior, Mid-Level, Senior)
       - Location preference (e.g., Dubai, Riyadh, Remote)
       - Core Skills (e.g., Python, PyTorch, SQL, Docker)
       - Key Projects & Certifications
    3. Tool Execution: Do NOT call `search_jobs` or `analyze_skill_gaps` until you have gathered at least their **industry/field**, **skills**, and **location**.
    4. Once you have enough data, invoke your tools to deliver data-driven match percentages and skill gap readiness reports. Keep your tone professional, encouraging, and razor-sharp.
    """)
    
    # Define Graph Node for the Agent
    def call_model(state: MessagesState):
        messages = state["messages"]
        # Ensure the system prompt is always at the beginning of the message history
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [system_prompt] + messages
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # Build the Explicit StateGraph Architecture
    workflow = StateGraph(MessagesState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    
    # Add  routing edges
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)  # Automatically routes to "tools" if tool calls are requested, else ends turn
    workflow.add_edge("tools", "agent")  # After tools run, return results back to the agent for final synthesis
    
    # Compile graph into an executable app
    app = workflow.compile()
    
    print("\n✨ TalentScout AI is live and interactive!")
    print("Tip: Have a natural conversation. Tell the agent your background, and it will guide you!")
    print("Type 'exit' or 'quit' to end the session.")
    
    # Interactive Multi-Turn Terminal Loop
    messages = []
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("\nTalentScout AI: Best of luck with your career journey and interviews! Goodbye.")
                break
                
            if not user_input.strip():
                continue
                
            # Append user message
            messages.append(("user", user_input))
            
            print("\nThinking...")
            # Invoke the LangGraph StateGraph app
            response = app.invoke({"messages": messages})
            
            # Extract latest assistant message from graph state
            latest_message = response["messages"][-1]
            agent_response = latest_message.content
            
            print(f"\nTalentScout AI:\n{agent_response}")
            
            # Update conversation history for multi-turn memory
            messages = response["messages"]
            
        except KeyboardInterrupt:
            print("\n\nTalentScout AI: Session ended. Goodbye!")
            break

if __name__ == "__main__":
    run_talent_scout()