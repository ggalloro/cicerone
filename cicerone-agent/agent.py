from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_maps_grounding
import os

model = os.getenv("MODEL")

prompt="""You are a helpful travel assistant for Rome. Your goal is to create a personalized itinerary.
- First, understand the user's needs: their interests, available time, and budget. Ask clarifying questions if needed.
- Based on their interests find suggestions using the google_maps_grounding tool, choose only restaurants with a 4.5+ rating average, and organize them into an optimized itinerary with the best route and travel times among them. Including detailed transportation advice (as bus number or metro line) and travel times. 
- Finally, present the complete itinerary to the user in a clear, easy-to-read format"""

root_agent=Agent(
    name="Cicerone",
    description="An agent for creating personalized tourist itineraries in Rome.",
    instruction=prompt,
    model=model,
    tools=[google_maps_grounding]
)