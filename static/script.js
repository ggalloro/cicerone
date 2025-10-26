document.getElementById('itinerary-form').addEventListener('submit', async function(event) {
    event.preventDefault();

            const city = document.getElementById('city').value;
            const interests = document.getElementById('interests').value;
            const budget = document.getElementById('budget').value;
            const time = document.getElementById('time').value;
    
            const prompt = `I want to plan a trip to ${city}. My interests are ${interests}. My budget is ${budget} and I have ${time} available.`;
    const responseDiv = document.getElementById('response');
    responseDiv.textContent = 'Generating itinerary...';

    const app_name = 'cicerone-agent';
    const user_id = 'user-123';
    const session_id = 'session-123';

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
});
