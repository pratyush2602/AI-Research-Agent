import asyncio
import os
from tavily import TavilyClient
from langchain_community.tools import TavilySearchResults
from groq import Groq
from langgraph.graph import StateGraph
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
search_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))

# Set up Groq API
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define Research Agent
async def research_agent(state):
    """Fetch research data using Tavily asynchronously."""
    query = state["query"]
    try:
        results = await asyncio.to_thread(search_tool.run, query)  # Run sync function in a separate thread
        print("Research Data start")
        print("---------------------------------------------------")
        print("Research Results:", results)
        print("---------------------------------------------------")
        print("Research Data end")
        return {"research_data": results}
    except Exception as e:
        print(f"Error during research: {e}")
        return {"research_data": None, "error": str(e)}

# Define Answer Drafting Agent
async def answer_drafting_agent(state):
    """Process research data and draft an answer using Groq LLM asynchronously."""
    research_data = state["research_data"]
    if not research_data:
        return {"answer": "No research data available to draft an answer."}
    
    prompt = f"""Based on the following research data, draft a comprehensive and well-structured response:
    {research_data}
    
    Please ensure the response is:
    - Clear and concise
    - Well-organized with headings and bullet points where appropriate
    - Supported by evidence from the research data
    - Free of jargon and accessible to a general audience
    """
    
    try:
        response = await asyncio.to_thread(
            lambda: groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "You are an AI research assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        print(f"Error during answer drafting: {e}")
        return {"answer": "Failed to draft an answer due to an error.", "error": str(e)}

# Define Review Agent
async def review_agent(state):
    """Review the drafted answer and provide feedback for improvement."""
    answer = state["answer"]
    if not answer or "Failed to draft" in answer:
        return {"reviewed_answer": answer, "feedback": "No answer to review."}
    
    prompt = f"""Review the following drafted answer and provide feedback for improvement:
    {answer}
    
    Please consider:
    - Clarity and coherence
    - Accuracy of information
    - Logical flow and structure
    - Grammar and readability
    """
    
    try:
        response = await asyncio.to_thread(
            lambda: groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "You are an AI reviewer."},
                    {"role": "user", "content": prompt}
                ]
            )
        )
        feedback = response.choices[0].message.content
        return {"reviewed_answer": answer, "feedback": feedback}
    except Exception as e:
        print(f"Error during review: {e}")
        return {"reviewed_answer": answer, "feedback": "Failed to review the answer due to an error.", "error": str(e)}

# Define Refinement Agent
async def refinement_agent(state):
    """Refine the answer based on the feedback."""
    answer = state["reviewed_answer"]
    feedback = state["feedback"]
    
    if not feedback or "Failed to review" in feedback:
        return {"final_answer": answer}
    
    prompt = f"""Refine the following answer based on the feedback provided:
    {answer}
    
    Feedback:
    {feedback}
    
    Please ensure the refined answer addresses all points in the feedback.
    """
    
    try:
        response = await asyncio.to_thread(
            lambda: groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "You are an AI refiner."},
                    {"role": "user", "content": prompt}
                ]
            )
        )
        return {"final_answer": response.choices[0].message.content}
    except Exception as e:
        print(f"Error during refinement: {e}")
        return {"final_answer": answer, "error": str(e)}

# Create LangGraph Workflow
workflow = StateGraph(dict) 

# Add agent nodes
workflow.add_node("research", research_agent)
workflow.add_node("draft_answer", answer_drafting_agent)
workflow.add_node("review_answer", review_agent)
workflow.add_node("refine_answer", refinement_agent)

# Define workflow execution flow
workflow.set_entry_point("research")
workflow.add_edge("research", "draft_answer")
workflow.add_edge("draft_answer", "review_answer")
workflow.add_edge("review_answer", "refine_answer")

# Set final node
workflow.set_finish_point("refine_answer")

# Compile workflow
research_system = workflow.compile()

# Run the Research AI Agentic System asynchronously
async def main():
    query = "What are the impacts of AI on the world"
    output = await research_system.ainvoke({"query": query})  
    print("\n=== Final Answer ===\n", output["final_answer"])

asyncio.run(main()) 