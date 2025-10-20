# Cicerone Romano

Cicerone Romano is a multi-agent system for creating personalized tourist itineraries in Rome. It uses a root agent, CiceroneRomano, that coordinates three specialized agents to provide tailored recommendations for art, food, and logistics.

## Application Capabilities

The application provides the following capabilities:

- **Personalized Art and History Recommendations:** The ArtHistorian agent suggests monuments, museums, and cultural sites based on the user's artistic and historical interests.
- **Tailored Culinary Suggestions:** The Gourmet agent recommends restaurants, trattorias, markets, and specialty food shops in line with the user's budget and culinary preferences.
- **Optimized Itinerary Planning:** The Logistics agent organizes the suggestions from the other agents into a coherent and optimized itinerary, estimating the best routes and travel times between points of interest.
- **Natural Language Interaction:** Users can interact with the application in natural language to specify their interests and receive a complete, easy-to-read itinerary.

## Structure

The application is structured as a multi-agent system using the Google Agent Development Kit (ADK).

- **`cicerone-agent/agent.py`**: This file contains the core logic of the application, including the definition of the four agents:
    - `CiceroneRomano`: The root agent that orchestrates the other agents.
    - `ArtHistorian`: The agent specialized in art and history.
    - `Gourmet`: The agent specialized in food and dining.
    - `Logistics`: The agent specialized in itinerary planning and logistics.
- **`requirements.txt`**: This file lists the Python dependencies of the application, which are `google-adk` and `python-dotenv`.
- **`.env`**: This file is used to store environment variables, such as the model name.

## How to Run Locally

To run the application locally, follow these steps:

1. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up the environment variables:**
   Create a `.env` file in the root of the project and add the following line:
   ```
   MODEL=gemini-2.5-flash
   ```
3. **Run the agent:**
   ```bash
   adk run cicerone-agent
   ```

## How to Test

To test the application, you can use the `adk` command-line interface. Once the agent is running, you can send messages to it to test its functionality. For example, you can send the following message to get a personalized itinerary:

```
"I'm interested in Renaissance art and I'm on a budget. Can you create an itinerary for me for a day in Rome?"
```

The agent will then process your request and provide a personalized itinerary with recommendations for art, food, and logistics.
