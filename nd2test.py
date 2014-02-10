from nicedice import *
roll = '2d5'
complexroll = '2dF+3'
wodroll = '4dW'
tests = [roll, complexroll, wodroll]
for roll in tests:
	print('Parsing '+roll)
	parse_roll(roll)

print("======")
print("RollGroup")
for roll in tests:
	print('Constructing '+roll)
	r = RollGroup(roll)
	#r.roll()
	print(r.result_string)
	r.roll()
	print(r.result_string)
