# Cicerone: an ADK Travel Agent with Google Maps grounding

I wanted to explore how an ADK agent would leverage Google Maps grounding so created this agent prototype to help users plan trips. The agent uses the Google Agent Development Kit (ADK) to build a personalized travel assistant. A key aspect of this project is the integration of the `google_maps_grounding` tool, which allows the agent to access real-world geographical data from Google Maps. The result is Cicerone, an agent designed to create tailored itineraries for any location.

![alt_text](img/Cicerone.png "image_tooltip")

### **Agent Implementation**

The complete code for this project is available on[ GitHub](https://github.com/ggalloro/cicerone).

The core of the application is a single travel planning agent named `Cicerone`, implemented using the `Agent` class from the Google ADK.

![alt_text](img/cicerone_diagram.png "image_tooltip")

I deliberately wanted to keep this very simple as a single agent to explore deeply the Google Maps grounding tool as the source of truth for attractions, locations, opening times, reviews, routes, travel times, etc…

A more structured travel assistant can be surely built as a multi-agent system leveraging different tools.

The agent is designed to understand a user’s travel needs from a structured JSON input containing the destination, interests, budget, and time. It then uses its tools to find relevant attractions, restaurants, and plan a route.

The agent’s prompt is dynamically generated from the user's JSON input, allowing it to generate itineraries for any location specified by the user. Here is the code from `agent.py` that defines the agent:

```python
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
        interests_str = ", ".join(interests) if isinstance(interests, list) else interests
        budget = data.get("budget", "")
        time = data.get("time", "")
        return f"""You are a helpful travel assistant. Your goal is to create a complete, personalized itinerary for a given location (city, region, or country) based on the user\'s preferences.
- The user wants to plan a trip to {location}. Their interests are {interests_str}. Their budget is {budget} and they have {time} available.
- Based on their interests, find suggestions for attractions and restaurants in the specified location using the google_maps_grounding tool.
- Choose only restaurants with a 4.5+ rating average.
- Organize the suggestions into a complete, optimized itinerary for the entire duration specified by the user.
- For each day, provide a schedule with the best route and travel times between locations, including detailed transportation advice (like bus numbers or metro lines).
- Present the final, complete itinerary in a clear, easy-to-read format. Do not ask for confirmation on each step; generate the full plan at once."""
    except (json.JSONDecodeError, KeyError):
        return """You are a helpful travel assistant. Your goal is to create a complete, personalized itinerary for a given location (city, region, or country) based on the user\'s preferences.
- Understand the user\'s needs from their initial prompt: the location they want to visit, their interests, available time, and budget.
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
```

### **The `google_maps_grounding` Tool**

A significant challenge in building AI travel planners is ensuring the information is accurate and up-to-date. The `Cicerone` agent's ability to provide detailed and practical travel information is powered by the `google_maps_grounding` tool. This tool addresses the challenge by connecting the agent directly to Google Maps, allowing it to access a vast amount of real-world geographical data.

With this tool, the agent can:

*   **Find Places:** Locate points of interest, such as museums, monuments, and restaurants, based on user queries.
*   **Get Place Details:** Retrieve information about specific locations, including ratings and other relevant details.
*   **Plan Routes:** Calculate travel times and get transportation suggestions between different points in the itinerary.

By grounding the agent’s responses in structured data from Google Maps, the `google_maps_grounding` tool enables the creation of itineraries that are not only personalized but also practical and reliable.

The source code for the tool can be found in the[ ADK Python repository on GitHub](https://github.com/google/adk-python/blob/main/src/google/adk/tools/google_maps_grounding_tool.py).

### **Testing the Agent with ADK Web**

The agent’s core logic can be tested directly using the ADK Web UI, which provides a simple interface for interacting with agents.

To test the agent, run the following command from the project’s root directory:

```bash
adk web
```

This will start the ADK Web UI. Select the `cicerone-agent` from the dropdown menu and introduce yourself or just say hello, the agent should ask information on the location you want to visit, your interests, budget and trip duration.

![alt_text](img/agent_prompt.png "image_tooltip")

After you provide the needed information the agent should then generate a complete itinerary based on your preferences.

![alt_text](img/cicerone_response_part.png "image_tooltip")

In the ADK Web UI you can also view, in the events, the google_maps_grounding tool response `groundingMetadata`:

![alt_text](img/grounding_metadata.png "image_tooltip")

### **Web Application**

To provide a more user-friendly experience, I also built a simple web application to serve the Cicerone agent.

The backend is a FastAPI web server that exposes the ADK agent. The frontend is a single-page application built with HTML, JavaScript, and Bootstrap.

It features a form where users can input their travel preferences. This information is then bundled into a JSON object and sent to the agent. The frontend handles user sessions by generating and storing a `user_id` in the browser's local storage, and creating a new `session_id` for each trip planning request. The generated itinerary is streamed from the backend and displayed on the page.

![alt_text](img/cicerone_webui.png "image_tooltip")

Here is the main code for the backend from `main.py`:
```python
import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=False
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

if __name__ == "__main__":
    # Use the PORT environment variable if available (for cloud deployments)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

Here is the main code for the frontend from `static/script.js`:
```javascript
document.getElementById('itinerary-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const location = document.getElementById('location').value;
    const interestsElement = document.getElementById('interests');
    const interests = Array.from(interestsElement.selectedOptions).map(option => option.value);
    const budget = document.getElementById('budget').value;
    const time = document.getElementById('time').value;

    const responseDiv = document.getElementById('response');
    responseDiv.textContent = 'Generating itinerary...';

    const app_name = 'cicerone-agent';

    function getOrSetUserId() {
        let userId = localStorage.getItem('cicerone_user_id');
        if (!userId) {
            userId = crypto.randomUUID();
            localStorage.setItem('cicerone_user_id', userId);
        }
        return userId;
    }

    const user_id = getOrSetUserId();
    const session_id = crypto.randomUUID();

    // Create or update the session
    await fetch(`/apps/${app_name}/users/${user_id}/sessions/${session_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ state: {} })
    });

    const response = await fetch('/run_sse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            app_name: app_name,
            user_id: user_id,
            session_id: session_id,
            new_message: {
                role: 'user',
                parts: [{ text: JSON.stringify({location, interests, budget, time}) }]
            }
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let result = '';
    responseDiv.innerHTML = ''; // Clear previous results

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        
        const lines = chunk.split('\n');
        for (const line of lines) {
            if (line.startsWith('data:')) {
                try {
                    const eventData = JSON.parse(line.substring(5));
                    if (eventData.content && eventData.content.parts[0].text) {
                        result += eventData.content.parts[0].text;
                    }
                } catch (e) {
                    // Ignore parsing errors
                }
            }
        }
        responseDiv.innerHTML = result.replace(/\n/g, '<br>');
    }
});
```


### **Conclusion**

This project demonstrates how the Google Agent Development Kit can be used to build a single-agent application and expose it through a web interface. The integration of the `google_maps_grounding` tool is a key aspect, showing how grounding an agent with structured, real-world data can significantly enhance its capabilities. The use of a structured, dynamic prompt allows the agent to provide information for travel planning for any location, and the architecture can be extended with more features and tools as needed as, for example:

*   Experimenting a multi-agent architecture (i wanted to focus on Google maps grounding in this example)
*   User registration/authentication and profiles
*   Possibility to save and modify itineraries

You can find the complete code for this project on[ GitHub](https://github.com/ggalloro/cicerone), where you can clone it to test it and make your own improvements.
