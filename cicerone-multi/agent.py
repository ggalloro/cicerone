import os
from google.adk.agents import LlmAgent
from google.adk.tools import google_search, google_maps_grounding
from google.adk.tools.agent_tool import AgentTool

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

art_historian_agent = LlmAgent(
    name="ArtHistorian",
    model=MODEL,
    instruction="""You are an art historian. Your task is to suggest monuments, museums, and cultural sites in Rome based on the user's artistic and historical interests.
    - Use the google_maps_grounding tool to find relevant locations.
    - Use the google_search tool to find interesting historical facts, opening hours, or information about specific artworks for the suggested locations to enrich the description.""",
    description="Suggests cultural sites in Rome based on user interests.",
    tools=[google_search, google_maps_grounding]
)

gourmet_agent = LlmAgent(
    name="Gourmet",
    model=MODEL,
    instruction="""You are a food critic in Rome. Your task is to suggest restaurants, trattorias, or markets based on the user's culinary preferences and budget.
    - Use the google_maps_grounding tool to find locations. Only consider places with an average rating of 4.5 or higher.
    - Use the google_search tool to find recent reviews or specialty dishes to justify your recommendations.""",
    description="Suggests dining and food experiences in Rome.",
    tools=[google_search, google_maps_grounding]
)

logistics_agent = LlmAgent(
    name="Logistics",
    model=MODEL,
    instruction="""You are a logistic expert. Your task is to create a coherent and optimized itinerary from a given list of points of interest.
    - Use the google_maps_grounding tool to estimate the best route and travel times between the locations.
    - Provide detailed transportation advice, including bus numbers or metro lines where appropriate.""",
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
- Finally, present the complete itinerary to the user in a clear, easy-to-read format, in the language used by the user for the request.""",
    description="A multi-agent system for creating personalized tourist itineraries in Rome.",
    tools=[
        AgentTool(agent=art_historian_agent),
        AgentTool(agent=gourmet_agent),
        AgentTool(agent=logistics_agent),
    ]
)
