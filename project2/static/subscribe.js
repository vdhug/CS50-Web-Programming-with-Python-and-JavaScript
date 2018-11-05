document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            var channelName = document.querySelector('#channelName').value;
            socket.emit('create channel', {'channelName': channelName});
        };
    });

   
});
