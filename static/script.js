document.addEventListener('DOMContentLoaded', () => {
    const itineraryForm = document.getElementById('itinerary-form');
    const responseDiv = document.getElementById('response');
    const saveButton = document.getElementById('save-button');
    const saveChangesButton = document.getElementById('save-changes-button');

    let itineraryGenerated = false;

    itineraryForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const interests = document.getElementById('interests').value;
        const budget = document.getElementById('budget').value;
        const time = document.getElementById('time').value;

        const prompt = `My interests are ${interests}. My budget is ${budget} and I have ${time} available.`;

        responseDiv.textContent = 'Generating itinerary...';
        responseDiv.setAttribute('contenteditable', 'false');
        saveButton.style.display = 'none';
        saveChangesButton.style.display = 'none';

        const app_name = 'cicerone-agent';
        const user_id = 'user-123';
        const session_id = 'session-123';

        // Create or update the session
        await fetch(`/apps/${app_name}/users/${user_id}/sessions/${session_id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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
                    parts: [{ text: prompt }]
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

        itineraryGenerated = true;
        responseDiv.setAttribute('contenteditable', 'true');
        saveButton.style.display = 'block';
    });

    responseDiv.addEventListener('input', () => {
        if (itineraryGenerated) {
            saveButton.style.display = 'none';
            saveChangesButton.style.display = 'block';
        }
    });

    saveButton.addEventListener('click', async () => {
        const itineraryContent = responseDiv.innerText;
        await saveItinerary(itineraryContent);
        alert('Itinerary saved!');
    });

    saveChangesButton.addEventListener('click', async () => {
        const itineraryContent = responseDiv.innerText;
        await saveItinerary(itineraryContent);
        alert('Changes saved!');
    });

    async function saveItinerary(content) {
        await fetch('/save-itinerary', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: 'session-123', // Using a static session id for simplicity
                content: content
            })
        });
    }
});
