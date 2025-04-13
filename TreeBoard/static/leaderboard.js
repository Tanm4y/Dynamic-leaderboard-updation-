// Establish WebSocket connection
const serverUrl = "ws://localhost:8765";  // Ensure this matches your WebSocket server's URL
let socket = new WebSocket(serverUrl);

// Handle connection open event
socket.onopen = function() {
    console.log("Connected to the WebSocket server.");
};

// Handle messages from the server
socket.onmessage = function(event) {
    console.log("Message received from server:", event.data);
    const playerData = JSON.parse(event.data);
    updateLeaderboard(playerData);
};

// Handle connection close event
socket.onclose = function(event) {
    if (event.wasClean) {
        console.log(`Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        console.error("Connection died unexpectedly");
    }
};

// Handle connection error
socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};

// Function to update the leaderboard
function updateLeaderboard(playerData) {
    const leaderboardElement = document.getElementById("leaderboard");

    // Check if player already exists on the leaderboard
    let existingEntry = document.getElementById(playerData.player_id);
    if (existingEntry) {
        // Update score if player already exists
        existingEntry.querySelector(".score").textContent = playerData.score;
    } else {
        // Create a new row for the new player
        const playerRow = document.createElement("tr");
        playerRow.id = playerData.player_id;

        // Player name column
        const nameCell = document.createElement("td");
        nameCell.textContent = playerData.player_id;
        playerRow.appendChild(nameCell);

        // Player score column
        const scoreCell = document.createElement("td");
        scoreCell.textContent = playerData.score;
        scoreCell.className = "score";
        playerRow.appendChild(scoreCell);

        // Add the new player row to the leaderboard
        leaderboardElement.appendChild(playerRow);
    }

    // Sort leaderboard rows based on scores in descending order
    sortLeaderboard();
}

// Function to sort the leaderboard
function sortLeaderboard() {
    const leaderboardElement = document.getElementById("leaderboard");
    const rows = Array.from(leaderboardElement.getElementsByTagName("tr"));

    rows.sort((a, b) => {
        const scoreA = parseInt(a.querySelector(".score").textContent);
        const scoreB = parseInt(b.querySelector(".score").textContent);
        return scoreB - scoreA;
    });

    // Append sorted rows back to leaderboard
    rows.forEach(row => leaderboardElement.appendChild(row));
}
