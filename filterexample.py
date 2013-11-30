integers = [-2,-1,0,1,2]

def greater_than_zero(x):
 	if x > 0:
 		return True
 	else:
 		return False


whole_numbers = [number for number in integers if greater_than_zero(number)]
print(whole_numbers)

def square(x):
	return x * x

squares = [square(number) for number in integers]
print(squares)

whole_squares = [square(number) for number in integers if greater_than_zero(number)]
print(whole_squares)