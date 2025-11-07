from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools import google_maps_grounding
import os
import json

model = os.getenv("MODEL", "gemini-2.5-flash")

def get_prompt(context: ReadonlyContext) -> str:
    user_input = context.user_content.parts[0].text
    try:
        data = json.loads(user_input)
        location = data.get("location", "")
        interests = data.get("interests", [])
        interests_str = ', '.join(interests) if isinstance(interests, list) else interests
        budget = data.get("budget", "")
        time = data.get("time", "")
        return f"""You are a helpful travel assistant. Your goal is to create a complete, personalized itinerary for a given location (city, region, or country) based on the user's preferences.
- The user wants to plan a trip to {location}. Their interests are {interests_str}. Their budget is {budget} and they have {time} available.
- Based on their interests, find suggestions for attractions and restaurants in the specified location using the google_maps_grounding tool.
- Choose only restaurants with a 4.5+ rating average.
- Organize the suggestions into a complete, optimized itinerary for the entire duration specified by the user.
- For each day, provide a schedule with the best route and travel times between locations, including detailed transportation advice (like bus numbers or metro lines).
- Present the final, complete itinerary in a clear, easy-to-read format. Do not ask for confirmation on each step; generate the full plan at once."""
    except (json.JSONDecodeError, KeyError):
        return """You are a helpful travel assistant. Your goal is to create a complete, personalized itinerary for a given location (city, region, or country) based on the user's preferences.
- Understand the user's needs from their initial prompt: the location they want to visit, their interests, available time, and budget.
- Based on their interests, find suggestions for attractions and restaurants in the specified location using the google_maps_grounding tool.
- Choose only restaurants with a 4.5+ rating average.
- Organize the suggestions into a complete, optimized itinerary for the entire duration specified by the user.
- For each day, provide a schedule with the best route and travel times between locations, including detailed transportation advice (like bus numbers or metro lines).
- Present the final, complete itinerary in a clear, easy-to-read format. Do not ask for confirmation on each step; generate the full plan at once."""

root_agent=Agent(
    name='cicerone_agent',
    description="An agent for creating personalized tourist itineraries for any location (city, region, or country).",
    instruction=get_prompt,
    model=model,
    tools=[google_maps_grounding]
)