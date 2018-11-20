document.addEventListener('DOMContentLoaded', () => {

	// Have each button change the color of the heading
    document.querySelectorAll('.pizza').forEach(function(button) {
        button.onclick = function() {
        	alert("ADDED" + button.id);
            return false;
        };
    });

    
});
