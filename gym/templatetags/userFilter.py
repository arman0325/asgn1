from django import template

register = template.Library()

@register.filter
def reId(value):
	if len(value)<7:
		s = value[0:2]+"***"+value[-1:]
	else:
		s = value[0:3]+"***"+value[-2:]
	return s

@register.filter
def reName(value):
	s = value.split()
	name=""
	for x in s:
		char = x[0]+"**** "
		name += char

	return name
