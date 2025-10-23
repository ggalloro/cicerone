from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_maps_grounding
import os

model = os.getenv("MODEL")

root_agent=Agent(
    name="Itinerary",
    description="Uses Google Maps grounding to provide an itinerary given a list of point of interest",
    instruction="Ask the user for a list of locations and provide an optimized itinerary using your google_maps_grounding tool",
    model=model,
    tools=[google_maps_grounding]
)