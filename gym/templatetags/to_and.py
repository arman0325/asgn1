from django import template

register = template.Library()

@register.filter
def to_and(value):
	if len(value)<7:
		s = value[0:3]+"***"
	else:
		s = value[0:3]+"*****"
	return s

@register.filter
def reName(value):
	s = value.split()
	name=""
	for x in s:
		char = x[0]+"**** "
		name += char

	return name
