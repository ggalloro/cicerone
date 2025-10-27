# Cicerone

Cicerone is an AI-based travel assistant that creates tourist itineraries for any location (city, region, or country). It uses a single agent to understand user preferences and generate a plan for a trip.

## Application Capabilities

The application provides the following capabilities:

- **Itinerary Generation for Any Location:** The agent takes a location, user interests, budget, and available time to generate an itinerary.
- **Location Suggestions:** The agent uses Google Maps to find attractions and restaurants that match user interests.
- **Route Planning:** The itinerary includes a schedule with routes, travel times, and public transportation advice.
- **Web Interface:** A web interface is provided to input travel preferences and view the generated itinerary.

## Structure

The application is built using the Google Agent Development Kit (ADK) and served via a FastAPI web server.

- **`cicerone-agent/`**: This directory contains the core ADK agent definition.
  - **`agent.py`**: Defines the `Cicerone` agent, its instructions, and the tools it uses.
- **`main.py`**: The FastAPI web server that exposes the agent and serves the frontend application.
- **`static/`**: Contains the frontend files.
  - **`index.html`**: The main HTML page with the user interface.
  - **`script.js`**: The JavaScript code that handles user input and communication with the agent's API.
- **`requirements.txt`**: Lists the Python dependencies for the project.
- **`.env`**: Used to store environment variables, such as API keys.

## How to Run Locally

To run the application locally, follow these steps:

1. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up the environment variables:**
   Create a `.env` file in the root of the project and add your Google API key:
   ```
   MODEL=gemini-2.5-flash
   # Add your Google API key if not using Vertex AI
   # GOOGLE_API_KEY=YOUR_API_KEY
   ```
3. **Run the web server:**
   ```bash
   python -m uvicorn main:app --reload
   ```
4. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000`.

## How to Use

1.  Open the web application in your browser.
2.  Fill in the form with the location you want to visit, your interests, budget, and the duration of your trip.
3.  Click the "Generate Itinerary" button.
4.  The agent will process your request and display an itinerary.
