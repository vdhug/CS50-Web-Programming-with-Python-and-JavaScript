
document.addEventListener('DOMContentLoaded', () => {

	var status_progress = document.getElementById("status-progress").value;

	if(status_progress === "place-order") {
		document.getElementById("status-place-order").classList.add("status-current");
	}

	if(status_progress === "finish") {
		document.getElementById("status-place-order").classList.add("status-current");
		document.getElementById("status-payment").classList.add("status-current");
	}

	document.querySelectorAll('.btn-cart').forEach(function(button) {
		button.onclick = function() { 
			const operation = button.dataset.operation;
			const progress = button.dataset.progress;
			debugger
			if(progress === "place-order" && operation=="next") {
				debugger
				var address = {
					
				};

				debugger
				$.ajax({
					url: '/update_progress',
					data:{
						operation: operation,
						street_name: document.getElementsByName("street-name")[0].value,
						street_number: document.getElementsByName("street-number")[0].value,
						apartment: document.getElementsByName("apartment")[0].value,
						reference: document.getElementsByName("reference")[0].value,
						postal_code: document.getElementsByName("postal-code")[0].value,
						neighborhoor: document.getElementsByName("neighborhoor")[0].value,
						city: document.getElementsByName("city")[0].value,
						state: document.getElementsByName("state")[0].value,
						progress: progress
					},
					success: function(data) {
						debugger
						location.reload()
					},
					failure: function(data) { 
						debugger
						alert('Got an error dude');
						return false;
					}
				});
			}
			else{
				$.ajax({
					url: '/update_progress',
					data:{
						operation: operation,
						progress: progress
					},
					success: function(data) {
						debugger
						location.reload()
					},
					failure: function(data) { 
						debugger
						alert('Got an error dude');
						return false;
					}
				});
			}
			
			debugger
			return false;
		};
	});


	// Have each button save the request to the session
	document.querySelectorAll('.item').forEach(function(input) {
		input.onchange = function() {
			// Get the type of the item (pizza, subs, pasta etc)
			const type = input.dataset.type;
			// Gets the id of the object of the type
			const type_id = input.dataset.id;

			// Gets the field that stores the quantity of items 
			var item_quantity = document.getElementById(type+"-"+type_id+"-quantity");
			
			// Checks if the actual quantity is less than 1, if true return false
			if (item_quantity.value <= 0){
				item_quantity.value = 1;
			}


			// Gets the field that stores the total value of the item
			var total_item = document.getElementById(type+"-"+type_id);

			// Gets the old total
			const old_total = total_item.dataset.total;

			// Gets the unit price of the item
			const unit_price = total_item.dataset.price;

			// Calculates the new total quantity * unit_price
			const new_total = unit_price * item_quantity.value;

			// Updates the inner html of the total of the item
			total_item.innerHTML = ""+new_total.toFixed(2) + " US";
			//Updates the value of total to the new value
			total_item.dataset.total = new_total;

			// Calculates the difference between the old total with the new total
			const diff = new_total- old_total;

			const old_quantity = parseInt(old_total/unit_price);

			$.ajax({
					url: '/edit_quantity',
					data:{
						price_id: type_id,
						old_quantity: old_quantity,
						new_quantity: item_quantity.value,
						item: type
					},
					success: function(data) {
						debugger
					},
					failure: function(data) { 
						debugger
						alert('Got an error dude');
						return false;
					}
			});

			// Gets the field that stores the total amount of the order
			var total_order = document.getElementById("total-amount");

			// Gets the old total value
			const old_total_order = total_order.dataset.total;
			debugger

			// Calculates the new total
			const new_total_order = parseFloat(old_total_order)+diff;

			// Updates the value of total to the new value
			total_order.dataset.total = new_total_order;

			// Updates the inner html of the total of the order
			total_order.innerHTML = ""+new_total_order.toFixed(2) + "<sup>US</sup>";
			

			return false;
		};
	});

	// Have each button save the request to the session
	document.querySelectorAll('.delete-item').forEach(function(button) {
		button.onclick = function() {
			// Get the type of the item (pizza, subs, pasta etc)
			const type = button.dataset.type;
			// Gets the id of the object of the type
			const type_id = button.dataset.id;

			const price = button.dataset.price;

			// Gets the field that stores the total amount of the order
			var total_order = document.getElementById("total-amount");

			// Gets the field that stores the total amount of the order
			var item = document.getElementById(type+"-"+type_id+"-ul");

			$.ajax({
					url: '/remove_item',
					data:{
						price_id: type_id,
						item: type
					},
					success: function(data) {
						debugger
						const total = (price * parseInt(data));
						const new_total = total_order.dataset.total - total;
						total_order.dataset.total = new_total;
						// Updates the inner html of the total of the order
						total_order.innerHTML = ""+new_total.toFixed(2) + "<sup>US</sup>";
						item.style.animationPlayState = 'running';
                    	item.addEventListener('animationend', () =>  {
                        item.remove();
                    });
						
					},
					failure: function(data) { 
						
						alert('Got an error dude');
						return false;
					}
				});

			return false;
		};
	});

	

	// Have each button save the request to the session
	document.querySelectorAll('.subtract').forEach(function(button) {
		button.onclick = function() {
			
			// Get the type of the item (pizza, subs, pasta etc)
			const type = button.dataset.type;
			// Gets the id of the object of the type
			const type_id = button.dataset.id;

			// Gets the field that stores the quantity of items 
			var item_quantity = document.getElementById(type+"-"+type_id+"-quantity");

			// Checks if the actual quantity is less than 1, if true return false
			if (item_quantity.value <= 1){
				return false;
			}
			const new_quantity =(parseInt(item_quantity.value) - 1);
			$.ajax({
					url: '/edit_quantity',
					data:{
						price_id: type_id,
						old_quantity: item_quantity.value,
						new_quantity: new_quantity,
						item: type
					},
					success: function(data) {
						debugger

						// Gets the field that stores the total amount of the order
						var total_order = document.getElementById("total-amount");
					},
					failure: function(data) { 
						debugger
						alert('Got an error dude');
						return false;
					}
			});
			// Updates the quantity that increased
			item_quantity.value = new_quantity;



			// Gets the field that stores the total value of the item
			var total_item = document.getElementById(type+"-"+type_id);

			// Gets the old total
			const old_total = total_item.dataset.total;

			// Gets the unit price of the item
			const unit_price = total_item.dataset.price;

			// Calculates the new total quantity * unit_price
			const new_total = unit_price * item_quantity.value;

			// Updates the inner html of the total of the item
			total_item.innerHTML = ""+new_total.toFixed(2) + " US";
			//Updates the value of total to the new value
			total_item.dataset.total = new_total;

			// Calculates the difference between the old total with the new total
			const diff = new_total- old_total;


			// Gets the field that stores the total amount of the order
			var total_order = document.getElementById("total-amount");

			// Gets the old total value
			const old_total_order = total_order.dataset.total;
			debugger

			// Calculates the new total
			const new_total_order = parseFloat(old_total_order)+diff;

			// Updates the value of total to the new value
			total_order.dataset.total = new_total_order;

			// Updates the inner html of the total of the order
			total_order.innerHTML = ""+new_total_order.toFixed(2) + "<sup>US</sup>";
			

			return false;
		};
	});

	// Have each button save the request to the session
	document.querySelectorAll('.add').forEach(function(button) {
		button.onclick = function() {

			// Get the type of the item (pizza, subs, pasta etc)
			const type = button.dataset.type;
			// Gets the id of the object of the type
			const type_id = button.dataset.id;

			// Gets the field that stores the quantity of items 
			var item_quantity = document.getElementById(type+"-"+type_id+"-quantity");
			
			// Updates the quantity that increased
			const new_quantity = ( parseInt(item_quantity.value) + 1);
			$.ajax({
					url: '/edit_quantity',
					data:{
						price_id: type_id,
						old_quantity: item_quantity.value,
						new_quantity: new_quantity,
						item: type
					},
					success: function(data) {
						debugger
					},
					failure: function(data) { 
						debugger
						alert('Got an error dude');
						return false;
					}
			});
			item_quantity.value = new_quantity;

			// Gets the field that stores the total value of the item
			var total_item = document.getElementById(type+"-"+type_id);

			// Gets the old total
			const old_total = total_item.dataset.total;

			// Gets the unit price of the item
			const unit_price = total_item.dataset.price;

			// Calculates the new total quantity * unit_price
			const new_total = unit_price * item_quantity.value;

			// Updates the inner html of the total of the item
			total_item.innerHTML = ""+new_total.toFixed(2) + " US";
			//Updates the value of total to the new value
			total_item.dataset.total = new_total;

			// Calculates the difference between the old total with the new total
			const diff = new_total- old_total;


			// Gets the field that stores the total amount of the order
			var total_order = document.getElementById("total-amount");

			// Gets the old total value
			const old_total_order = total_order.dataset.total;
			debugger

			// Calculates the new total
			const new_total_order = parseFloat(old_total_order)+diff;

			// Updates the value of total to the new value
			total_order.dataset.total = new_total_order;

			// Updates the inner html of the total of the order
			total_order.innerHTML = ""+new_total_order.toFixed(2) + "<sup>US</sup>";
			

			return false;
		};
	});

	// Have each button save the request to the session
	document.querySelectorAll('.btn-cart-finish').forEach(function(button) {
		button.onclick = function() {
			
			// Select the ul that contains all the toppings from this pizza
			var items = []
			var pizzas = document.querySelectorAll('.pizza-details');
			pizzas.forEach(function(pizza) {
				const pizza_id = pizza.dataset.id;

				// Select the li that contains the options
				const options = pizza.children;
				var toppings = [];

				for (i=1; i<options.length; i++){
					var topping = options[i].children[0].value;
					toppings.push(topping);
				}
				var item_order = {key: pizza_id, value: toppings};
				items.push(item_order)
				
				
			});
			var jsonText = JSON.stringify(items)
			debugger
			$.ajax({
					url: '/submit_order',
					csrfmiddlewaretoken: '{{ csrf_token }}',
					type: 'POST',
					data: {
						items: jsonText
					},
					success: function(data) {
						debugger
						location.reload()
					},
					failure: function(data) { 
						debugger
						alert('Got an error dude');
						return false;
					}
			});
			return false;
		};
	});

});
