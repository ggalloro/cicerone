# Cicerone

Cicerone is an AI-powered travel assistant that creates personalized tourist itineraries for any city in the world. It uses a single, powerful agent to understand your preferences and generate a detailed plan for your trip.

## Application Capabilities

The application provides the following capabilities:

- **Personalized Itineraries for Any City:** Simply tell the agent which city you want to visit, your interests, budget, and available time, and it will generate a custom itinerary for you.
- **Detailed Suggestions:** The agent uses Google Maps to find attractions and highly-rated restaurants that match your interests.
- **Optimized Planning:** The itinerary includes an optimized schedule with routes, travel times, and public transportation advice (like bus or metro lines).
- **Web Interface:** An intuitive web interface allows you to easily input your travel preferences and view the generated itinerary.
- **Save and Modify:** You can edit the generated itinerary directly in the browser and save it for later use.

## Structure

The application is built using the Google Agent Development Kit (ADK) and served via a FastAPI web server.

- **`cicerone-agent/`**: This directory contains the core ADK agent definition.
  - **`agent.py`**: Defines the `Cicerone` agent, its instructions, and the tools it uses.
- **`main.py`**: The FastAPI web server that exposes the agent and serves the frontend application.
- **`static/`**: Contains the frontend files.
  - **`index.html`**: The main HTML page with the user interface.
  - **`script.js`**: The JavaScript code that handles user input and communication with the agent's API.
- **`itineraries/`**: The directory where saved itineraries are stored as text files.
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
2.  Fill in the form with the city you want to visit, your interests, budget, and the duration of your trip.
3.  Click the "Generate Itinerary" button.
4.  The agent will process your request and display a complete itinerary.
5.  You can then edit the itinerary directly on the page and save it using the "Save Changes" button.
