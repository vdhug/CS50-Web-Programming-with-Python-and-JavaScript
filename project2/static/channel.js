document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const name = document.getElementById("channelName").value;
                alert("SOCKET TRIGGERED")
                var result = socket.emit('create channel', {'id': 0, 'name': name});
                
            };
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('channel created', data => {
        alert("EMIT")
        // Find a <table> element with id="channels":
        var table = document.getElementById("channels");

        // Create an empty <tr> element and add it to the 1st position of the table:
        var row = table.insertRow(-1);

        // Insert new cells (<td> elements) at the 1st position of the "new" <tr> element:
        var cell1 = row.insertCell(0);

        // Add some text to the new cell:
        cell1.innerHTML = data["name"];
    });
});
