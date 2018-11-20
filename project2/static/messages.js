document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                var channel_id = document.getElementById("channel_id").value;
                var message = document.getElementById("message").value;

                socket.emit('send message', {'channel_id': channel_id, 'message': message});
                return false;
            };
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('message received', data => {
        // Find a <table> element with id="channels":
        var table = document.getElementById("messages");

        // Create an empty <tr> element and add it to the 1st position of the table:
        var row = table.insertRow(0);

        // Insert new cells (<td> elements) at the 1st position of the "new" <tr> element:
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);

        // Add some text to the new cell:
        cell1.innerHTML = data["user_id"];
        cell2.innerHTML = data['message'];
        return false;
    });
});