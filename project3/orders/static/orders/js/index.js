
document.addEventListener('DOMContentLoaded', () => {

	// Have each button save the request to the session
	document.querySelectorAll('.item').forEach(function(button) {
		button.onclick = function() {
			// Initialize new request
			
			const price_id = button.dataset.id;
			const item_type = button.dataset.type;
			const operation = button.dataset.operation;
			button.disabled = true;
			if(operation === "add") {
				$.ajax({
					url: '/add_item',
					data:{
						price_id: price_id,
						item: item_type
					},
					success: function(data) {
						button.disabled = false;
						button.title = "Remove from the cart";
						button.classList.add("itemIsSelected");
						button.dataset.operation = "remove";
					},
					failure: function(data) { 
						button.disabled = false;
						alert('Got an error dude');
					}
				});
			}
			debugger
			if(operation === "remove") {
				$.ajax({
					url: '/remove_item',
					data:{
						price_id: price_id,
						item: item_type
					},
					success: function(data) {
						debugger
						button.title = "Add to the cart";
						button.classList.remove("itemIsSelected");
						button.dataset.operation = "add";
					},
					failure: function(data) { 
						
						alert('Got an error dude');
					}
				});
			}
			
			
			return false;
		};
	});

	
	
});
