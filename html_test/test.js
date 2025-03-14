const url = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-US";
const headers = {
    "Accept": "application/json",
    "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
};
const urlPast = "https://lolesports.com/api/gql?operationName=homeEvents&variables=%7B%22hl%22%3A%22fr-FR%22%2C%22sport%22%3A%22lol%22%2C%22eventState%22%3A%5B%22completed%22%5D%2C%22eventType%22%3A%22match%22%2C%22pageSize%22%3A40%2C%22pageToken%22%3A%22b2xkZXI6OjExMzQ3NjA1NDQ1MDU1ODg3Nw%3D%3D%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22089916a64423fe9796f6e81b30e9bda7e329366a5b06029748c610a8e486d23f%22%7D%7D"


let allEvents = [];  // Store all events for filtering

async function fetchSchedule() {
    try {   
        const response = await fetch(url, { method: "GET", headers });
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        allEvents = data.data.schedule.events;  // Store all events
        populateLeagues(allEvents);           // Populate league options
        displaySchedule(allEvents);           // Display all events by default
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("upcoming-matches").innerText = "Failed to load schedule.";
        document.getElementById("past-matches").innerText = "Failed to load matches.";
    }
}

function populateLeagues(events) {
    const leagueFilter = document.getElementById("league-filter");

    // Extract all unique league names
    const leagues = Array.from(new Set(events.map(event => event.league?.name)));

    // Add "All Leagues" option manually
    const allOption = document.createElement("option");
    allOption.value = "all";
    allOption.innerText = "All Leagues";
    leagueFilter.appendChild(allOption);

    // Add options for the leagues dynamically
    leagues.forEach(league => {
        const option = document.createElement("option");
        option.value = league;
        option.innerText = league;
        leagueFilter.appendChild(option);
    });

    // Set up event listener for league filter
    leagueFilter.addEventListener("change", (e) => {
        const selectedLeague = e.target.value;
        const filteredEvents = selectedLeague === "all" ? events : events.filter(event => event.league?.name === selectedLeague);
        displaySchedule(filteredEvents);
    });
}

function displaySchedule(events) {
    const now = new Date();
    const upcomingContainer = document.getElementById("upcoming-matches");
    const pastContainer = document.getElementById("past-matches");

    upcomingContainer.innerHTML = "";
    pastContainer.innerHTML = "";

    const upcomingMatches = events.filter(event => new Date(event.startTime) > now);
    const pastMatches = events.filter(event => new Date(event.startTime) <= now);

    if (upcomingMatches.length === 0) {
        upcomingContainer.innerHTML = "<p>No upcoming matches found.</p>";
    } else {
        upcomingMatches.forEach(event => renderMatch(event, upcomingContainer));
    }

    if (pastMatches.length === 0) {
        pastContainer.innerHTML = "<p>No past matches found.</p>";
    } else {
        pastMatches.forEach(event => renderMatch(event, pastContainer, true));
    }
}

function renderMatch(event, container, isPast = false) {
    if (!event.match || !event.match.teams) return;

    const [team1, team2] = event.match.teams;

    const matchCard = document.createElement('div');
    matchCard.classList.add('match-card');
    if (isPast) matchCard.classList.add('past-match');

    matchCard.innerHTML = `
        <div class="league-name">${event.league?.name || "Unknown League"} - ${event.blockName || ""}</div>
        <div class="teams">
            <div class="team">
                <img src="${team1.image || ''}" alt="${team1.name}" class="${team1.result?.outcome === 'win' ? 'winner' : 'loser'}" />
                <div class="team-name">${team1.name}</div>
                <div class="score">${team1.result?.gameWins ?? 0}</div>
            </div>
            <div class="team">
                <img src="${team2.image || ''}" alt="${team2.name}" class="${team2.result?.outcome === 'win' ? 'winner' : 'loser'}" />
                <div class="team-name">${team2.name}</div>
                <div class="score">${team2.result?.gameWins ?? 0}</div>
            </div>
        </div>
        <div class="match-info">
            Best of <span>${event.match.strategy?.count || "?"}</span> | 
            <span>${new Date(event.startTime).toLocaleString()}</span>
        </div>
    `;

    container.appendChild(matchCard);
}

fetchSchedule();
