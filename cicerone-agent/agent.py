import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_maps_grounding

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

art_historian_agent = LlmAgent(
    name="ArtHistorian",
    model=MODEL,
    instruction="""You are an art historian. Suggest monuments, museums, and cultural sites in Rome based on the user's artistic and historical interests.
    Use Google Search to find up-to-date information on temporary exhibitions and special events.""",
    description="Suggests cultural sites in Rome based on user interests.",
    tools=[google_search]
)

gourmet_agent = LlmAgent(
    name="Gourmet",
    model=MODEL,
    instruction="""You are a food critic. Suggest restaurants, trattorias, markets, and specialty food shops in Rome in line with the user's budget and culinary preferences.
    Use Google Search to find recent reviews, price ranges, and specialties.""",
    description="Suggests dining and food experiences in Rome.",
    tools=[google_search]
)

logistics_agent = LlmAgent(
    name="Logistics",
    model=MODEL,
    instruction="""You are a logistic expert. Organize the suggestions from the other agents into a coherent and optimized itinerary.
    Estimate the best route and travel times between the places suggesteed by the other 2 agents using the google_maps_grounding tool. Return routes, transportation advice and travel times.""",
    description="Organizes suggestions into a structured itinerary.",
    tools=[google_maps_grounding]
)


root_agent = LlmAgent(
    name="Cicerone",
    model=MODEL,
    instruction="""You are a helpful travel assistant for Rome. Your goal is to create a personalized itinerary.
- First, understand the user's needs: their interests, available time, and budget. Ask clarifying questions if needed.
- Based on their interests, use the 'ArtHistorian' and 'Gourmet' tools to find suggestions.
- Once you have all the suggestions, use the 'Logistics' tool to organize them into a coherent plan with routes, transportation advice and travel times. 
- Finally, present the complete itinerary to the user in a clear, easy-to-read format, in the language used by the user for the request""",
    description="A multi-agent system for creating personalized tourist itineraries in Rome.",
    tools=[
        AgentTool(agent=art_historian_agent),
        AgentTool(agent=gourmet_agent),
        AgentTool(agent=logistics_agent),
    ]
)
