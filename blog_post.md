# [blog] Cicerone: an ADK Travel Agent with Google Maps grounding

I wanted to explore how an ADK agent would leverage Google Maps grounding so created this agent prototype to help users plan trips. The agent uses the Google Agent Development Kit (ADK) to build a personalized travel assistant. A key aspect of this project is the integration of the `google_maps_grounding` tool, which allows the agent to access real-world geographical data from Google Maps. The result is Cicerone, an agent designed to create tailored itineraries for any location.


![alt_text](img/Cicerone.png "image_tooltip")



### **Agent Implementation**

The complete code for this project is available on[ GitHub](https://github.com/ggalloro/cicerone).

The core of the application is a single travel planning agent named `Cicerone`, implemented using the `Agent` class from the Google ADK.


![alt_text](img/cicerone_diagram.png "image_tooltip")


I deliberately wanted to keep this very simple as a single agent to explore deeply the Google Maps grounding tool as the source of truth for attractions, locations, opening times, reviews, routes, travel times, etc…

A more structured travel assistant can be surely built as a multi-agent system leveraging different tools.

The agent is designed to understand a user’s travel needs — including the destination, interests, budget, and time — from a single prompt. It then uses its tools to find relevant attractions, restaurants, and plan a route.

The agent’s prompt is written to be location-agnostic, allowing it to generate itineraries for any location specified by the user. Here is the code from `agent.py` that defines the agent:


### **The <code>google_maps_grounding</code> Tool**

A significant challenge in building AI travel planners is ensuring the information is accurate and up-to-date. The `Cicerone` agent's ability to provide detailed and practical travel information is powered by the `google_maps_grounding` tool. This tool addresses the challenge by connecting the agent directly to Google Maps, allowing it to access a vast amount of real-world geographical data.

With this tool, the agent can:



* **Find Places:** Locate points of interest, such as museums, monuments, and restaurants, based on user queries.
* **Get Place Details:** Retrieve information about specific locations, including ratings and other relevant details.
* **Plan Routes:** Calculate travel times and get transportation suggestions between different points in the itinerary.

By grounding the agent’s responses in structured data from Google Maps, the `google_maps_grounding` tool enables the creation of itineraries that are not only personalized but also practical and reliable.

The source code for the tool can be found in the[ ADK Python repository on GitHub](https://github.com/google/adk-python/blob/main/src/google/adk/tools/google_maps_grounding_tool.py).


### **Testing the Agent with ADK Web**

The agent’s core logic can be tested directly using the ADK Web UI, which provides a simple interface for interacting with agents.

To test the agent, run the following command from the project’s root directory:

adk web

This will start the ADK Web UI. Select the `cicerone-agent` from the dropdown menu and introduce yourself or just say hello, the agent should ask information on the location you want to visit, your interests, budget and trip duration.


![alt_text](img/agent_prompt.png "image_tooltip")


After you provide the needed information the agent should then generate a complete 3-day itinerary for Rome based on these preferences.


![alt_text](img/cicerone_response_part.png "image_tooltip")


In the ADK Web UI you can also view, in the events, the google_maps_grounding tool response `groundingMetadata` field including `groundingChunks`: arrays of objects containing the maps sources (`uri`, `placeId` and `title`):


![alt_text](img/grounding_metadata.png "image_tooltip")



### **Web Application**

To provide a more user-friendly experience, I also built a simple web application to serve the Cicerone agent.

The backend is a FastAPI web server that exposes the ADK agent. The frontend is a single-page application built with HTML, JavaScript, and Bootstrap. 

It features a form where users can input their travel preferences. This information is then sent to the agent, and the generated itinerary is displayed on the page.


![alt_text](img/cicerone_webui.png "image_tooltip")



### **Conclusion**

This project demonstrates how the Google Agent Development Kit can be used to build a single-agent application and expose it through a web interface. The integration of the `google_maps_grounding` tool is a key aspect, showing how grounding an agent with structured, real-world data can significantly enhance its capabilities. The use of a generalized prompt allows the agent to provide information for travel planning for any location, and the architecture can be extended with more features and tools as needed as, for example:



* Experimenting a multi-agent architecture (i wanted to focus on Google maps grounding in this example)
* User registration/authentication and profiles
* Possibility to save and modify itineraries

You can find the complete code for this project on[ GitHub](https://github.com/ggalloro/cicerone), where you can clone it to test it and make your own improvements.
