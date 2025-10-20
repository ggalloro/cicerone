# Building a Multi-Agent Travel Assistant for Rome with Google's ADK

I've been thinking for a while about creating a tool to help tourists navigate the rich history and culture of Rome. This led me to explore the Google Agent Development Kit (ADK) to build a personalized travel assistant. The ADK is a framework for building, evaluating, and deploying agents. It provides a set of tools and libraries that simplify the development process. This blog post describes the result: Cicerone Romano, a multi-agent system designed to create tailored itineraries for visitors to the Eternal City.

## A Multi-Agent Architecture for Personalized Itineraries

The Cicerone Romano agent uses a multi-agent architecture to handle the different aspects of travel planning. A root agent, `CiceroneRomano`, coordinates the work of three specialized agents:

- **`ArtHistorian`**: This agent is responsible for suggesting monuments, museums, and cultural sites based on the user's artistic and historical interests.
- **`Gourmet`**: This agent focuses on the culinary aspect of the trip, recommending restaurants, markets, and food shops that match the user's budget and preferences.
- **`Logistics`**: This agent takes the suggestions from the `ArtHistorian` and `Gourmet` agents and organizes them into a coherent and optimized itinerary.

This separation of concerns allows each agent to focus on a specific task, leading to more accurate and relevant recommendations.

## Agent Implementation with the ADK

The agents are implemented using the `LlmAgent` class from the Google ADK. Here is a code snippet from `agent.py` that shows how the `ArtHistorian` agent is defined:

```python
art_historian_agent = LlmAgent(
    name="ArtHistorian",
    model=MODEL,
    instruction="""You are an art historian. Suggest monuments, museums, and cultural sites in Rome based on the user's artistic and historical interests.
    Use Google Search to find up-to-date information on temporary exhibitions and special events.""",
    description="Suggests cultural sites in Rome based on user interests.",
    tools=[google_search]
)
```

The `Gourmet` agent is defined in a similar way:

```python
gourmet_agent = LlmAgent(
    name="Gourmet",
    model=MODEL,
    instruction="""You are a food critic. Suggest restaurants, trattorias, markets, and specialty food shops in Rome in line with the user's budget and culinary preferences.
    Use Google Search to find recent reviews, price ranges, and specialties.""",
    description="Suggests dining and food experiences in Rome.",
    tools=[google_search]
)
```

The `CiceroneRomano` root agent uses the other agents as tools:

```python
root_agent = LlmAgent(
    name="CiceroneRomano",
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
```

## The `google_maps_grounding` Tool

The `Logistics` agent uses the new `google_maps_grounding` tool to create the itinerary. This tool allows the agent to estimate the best route and travel times between points of interest. The tool's implementation can be found in the `adk-python` repository on GitHub: [https://github.com/google/adk-python/blob/main/src/google/adk/tools/google_maps_grounding_tool.py](https://github.com/google/adk-python/blob/main/src/google/adk/tools/google_maps_grounding_tool.py)

Here is how the `Logistics` agent is defined to use the `google_maps_grounding` tool:

```python
logistics_agent = LlmAgent(
    name="Logistics",
    model=MODEL,
    instruction="""You are a logistic expert. Organize the suggestions from the other agents into a coherent and optimized itinerary.
    Estimate the best route and travel times between points of interest using Google Maps grounding tool. Return routes, transportation advice and travel times.""",
    description="Organizes suggestions into a structured itinerary.",
    tools=[google_maps_grounding]
)
```

## Generalization and Conclusion

While the Cicerone Romano agent is specific to Rome, the underlying architecture can be generalized to create a travel assistant for any city. By replacing the Rome-specific instructions with more general ones and providing the agent with the ability to identify the user's desired location, the same multi-agent approach can be used to create a flexible and powerful travel planning tool.

This example demonstrates how the Google Agent Development Kit can be used to build a sophisticated, multi-agent system for a real-world application. The new `google_maps_grounding` tool, in particular, opens up new possibilities for creating location-aware and contextually relevant agents.
