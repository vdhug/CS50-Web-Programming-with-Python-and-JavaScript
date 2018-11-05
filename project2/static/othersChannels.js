document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When a new vote is announced, add to the unordered list
    socket.on('channel created', data => {
        // Find a <table> element with id="channels":
        var table = document.getElementById("channels");

        // Create an empty <tr> element and add it to the 1st position of the table:
        var row = table.insertRow(0);

        // Insert new cells (<td> elements) at the 1st position of the "new" <tr> element:
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);

        // Add some text to the new cell:
        cell1.innerHTML = data["name"];
        cell2.innerHTML = "<a href=channel/"+ data['id'] +">Join Channel</a>";

        return false;
    });
});
