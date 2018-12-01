from django.db import models
from django.contrib.auth.models import User

# Class that defines the types of pizza that exist in this restaurant
class TypeOfPizza(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return f"{self.name}"

# Class that defines the sizes existing in this restaurant
class Size(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return f"{self.name}"


class SizeOfPizza(models.Model):
	size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="sizeOfPizzas")
	typeOfPizza = models.ForeignKey(TypeOfPizza, on_delete=models.CASCADE)
	description = models.CharField(max_length=128)

	def __str__(self):
		return f"{self.size} - {self.typeOfPizza}"


# Class that defines the pizza existing in the restaurant
class Pizza(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(default="")
	custom = models.BooleanField(default=False)
	numberOfToppings = models.IntegerField(default=0)
	
	prices = models.ManyToManyField(SizeOfPizza, through='PriceOfPizza')

	def __str__(self):
		return f"{self.name}"


# Class that defines the size and price of the pizzas
class PriceOfPizza(models.Model):
	sizeOfPizza = models.ForeignKey(SizeOfPizza, on_delete=models.CASCADE)
	pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="prices_of_pizza")
	price = models.DecimalField(max_digits=6, decimal_places=2)
	def __str__(self):
		return f"{self.sizeOfPizza} - {self.pizza.name} - {self.price}"

# Class that defines the Subs available in this restaurant
class Sub(models.Model):
	name = models.CharField(max_length=64)
	prices = models.ManyToManyField(Size, through='PriceOfSub')

	def __str__(self):
		return f"{self.name}"


# Class that defines the size and price of the subs
class PriceOfSub(models.Model):
	size = models.ForeignKey(Size, on_delete=models.CASCADE)
	sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="prices_of_sub")
	price = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return f"{self.size} - {self.price} U$"


# Class that defines the Dinners available in this restaurant
class Dinner(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(default="")
	prices = models.ManyToManyField(Size, through='PriceOfDinner')

	def __str__(self):
		return f"{self.name} - Prices: {self.prices}"


# Class that defines the size and price of the subs
class PriceOfDinner(models.Model):
	size = models.ForeignKey(Size, on_delete=models.CASCADE)
	dinner = models.ForeignKey(Dinner, on_delete=models.CASCADE, related_name="prices_of_dinner")
	price = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return f"{self.size} - {self.price} U$"


# Class that defines the toppings available in this restaurant
class Topping(models.Model):
	name = models.CharField(max_length=64)
	def __str__(self):
		return f"{self.name}"

# Class that defines the pasta available in this restaurant
class Pasta(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(default="")
	price = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return f"{self.name} - {self.price} U$"


# Class that defines the salads available in this restaurant
class Salad(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(default="")
	price = models.DecimalField(max_digits=6, decimal_places=2)
	
	def __str__(self):
		return f"{self.name} - {self.price} U$"


class Order(models.Model):
	total = models.DecimalField(max_digits=6, decimal_places=2)
	date_submitted = models.DateField(auto_now_add=True)
	date_delivered = models.DateField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

	STATUS_ORDER_CHOICES = (
		('SUBMITTED', 'Submitted'),
		('PRODUCTION', 'In Production'),
		('DELIVERING', 'Left to Deliver'),
		('DELIVERED', 'Delivered'),
		('CANCELLED', 'Cancelled'),
	)
	status_order = models.CharField(
		max_length=50,
		choices=STATUS_ORDER_CHOICES,
		default='SUBMITTED',
	)

	def __str__(self):
		return f"{self.user.username} - {self.status_order} "


class ItemOrder(models.Model):
	description = models.TextField(default="")
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

	def __str__(self):
		return f"{self.order.user.username} - {self.description} - {self.quantity} - {self.price}"