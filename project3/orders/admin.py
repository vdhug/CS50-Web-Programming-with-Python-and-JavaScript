from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(TypeOfPizza)
admin.site.register(Size)
admin.site.register(SizeOfPizza)
admin.site.register(Pizza)
admin.site.register(PriceOfPizza)
admin.site.register(ItemOrder)
admin.site.register(Order)
admin.site.register(Sub)
admin.site.register(PriceOfSub)
admin.site.register(Dinner)
admin.site.register(PriceOfDinner)
admin.site.register(Topping)
admin.site.register(Pasta)
admin.site.register(Salad)