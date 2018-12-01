from django.template import Library

register = Library()

@register.filter
def get_range(value):
	return range(value)

@register.filter
def get_add(value, arg):
	return value+arg

@register.filter
def isGreaterThanZero(value):
	return value>0

@register.filter
def get_multiply(value, arg):
	return value*arg

@register.filter
def stringIsEqual(value, arg):
	return value==arg

@register.filter
def stringIsDifferent(value, arg):
	return value!=arg