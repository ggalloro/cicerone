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
