# libraries
import numpy as np 
import matplotlib.pyplot as plt 
plt.style.use('dark_background')

def successive_approximations(x_start, iterations):
	'''
	Computes the successive approximations for the equation
	y = x^3 - 1.
	'''
	x_now = x_start
	ls = []
	for i in range(iterations):
		f_now = x_now**3 - 1
		f_prime_now = 3*x_now**2 

		x_next = x_now - f_now / f_prime_now
		ls.append(x_now)
		x_now = x_next
	return ls


# print (successive_approximations(2 + 5j, 20))


class Calculate:

	def __init__(self, equation, point, differentiate=False):
		self.equation = equation
		self.point = point
		self.diff = differentiate

	def parse(self):
		equation = self.equation
		digits = '0123456789.'
		characters_ls = [i for i in equation]
		characters_ls = ['start'] + characters_ls
		characters_ls.append('end')
		for i in range(len(characters_ls)-1):
			if characters_ls[i] not in digits and characters_ls[i+1] == 'x':
				characters_ls.insert(i+1, '1')
		ls, i = [], 0

		# parse expression into list
		while i in range(len(characters_ls)):
			if characters_ls[i] in digits:
				number = ''
				j = 0
				while characters_ls[i+j] in digits:
					number += (characters_ls[i+j])
					j += 1
				ls.append(float(number))
				i += j
			else:
				ls.append(characters_ls[i])
				i += 1

		return ls

	def differentiate(self):
		'''
		A helper function that finds the derivative of a given
		function 'equation' and computes this derivative at
		value 'point'.  Accepts any polynomial with positive
		exponent values.
		'''
		parsed_exp = self.parse()
		ls, point = parsed_exp, self.point

		# differentiate polynomial
		final_ls = []
		for i in range(len(ls)):

			if isinstance(ls[i], float) and ls[i+1] == 'x' or ls[i-1] == '^' and ls[i-2] == 'x':
				final_ls.append(ls[i])

			if ls[i] == 'x':
				if ls[i+1] == '^':
					final_ls[-1] *= ls[i+2]
					if ls[i+2] > 0: # prevent divide by 0 error
						ls[i+2] -= 1 
				final_ls.append(ls[i])

			if ls[i]== 'x' and ls[i+1] != '^':
				final_ls.append('^')
				final_ls.append(0)

			if ls[i] in ['+', '-', '^']:
				final_ls.append(ls[i])

		while True:
			if isinstance(final_ls[-1], float):
				break
			final_ls.pop()
		final_ls.append('+')

		return final_ls


	def evaluate(self):
		'''
		A helper function that finds the derivative of a given
		function 'equation' and computes this derivative at
		value 'point'. Note that this point may also be an ogrid
		value, in which case the derivative is computed at each
		point on the grid. Accepts any polynomial with positive
		exponent values.
		'''
		if self.diff:
			final_ls = self.differentiate()
		else:
			final_ls = self.parse()

		if final_ls[0] != 'start':
			final_ls = ['start'] + final_ls
		if final_ls[-1] != 'end':
			final_ls.append('end')
		final_ls[0], final_ls[-1] = '+', '+' # change 'start' and 'end' to appropriate markers

		point =self.point
		# evaluate parsed expression
		i = 0
		final_blocks = [[]]
		while i in range(len(final_ls)):
			ls = []
			j = 0
			while final_ls[i+j] not in ['+', '-']:
				ls.append(final_ls[i+j])
				j += 1
			if final_ls[i-1] == '-':
				if ls:
					ls[0] = -1 * ls[0]
			final_blocks.append(ls)
			i += j + 1

		total = 0
		for block in final_blocks:
			if block:
				if '^' not in block:
					if 'x' not in block:
						block += ['x', '^', 0]
					else:
						block += ['^', 1]

				start = block[0] * point ** block[-1]
				total += start

		return total

def newton_raphson_map(equation, max_iterations, x_range, y_range, t):
	print (equation)
	xl = -10/(2**(t/30)) + 0.41187
	xr = 10/(2**(t/30)) + 0.41187
	yl = 10/(2**(t/30))
	yr = -10/(2**(t/30)) 
	y, x = np.ogrid[yl: yr: y_range*1j, xl: xr: x_range*1j]
	z_array = x + y*1j

	iterations_until_rooted = max_iterations + np.zeros(z_array.shape)
	 # create a boolean table of all 'true'
	not_already_at_root = iterations_until_rooted < 10000

	for i in range(max_iterations):
		previous_z_array = z_array
		z = z_array
		f_now = Calculate(equation, z, differentiate=False).evaluate()
		f_prime_now = Calculate(equation, z, differentiate=True).evaluate()
		# f_now = z**5-z-1
		# f_prime_now = 5*z**4-1
		z_array = z_array - f_now / f_prime_now

		# the boolean map is tested for rooted values
		found_root = (abs(z_array - previous_z_array) < 0.0000001) & not_already_at_root
		iterations_until_rooted[found_root] = i
		not_already_at_root = np.invert(found_root) & not_already_at_root

	return iterations_until_rooted

plt.imshow(newton_raphson_map('x^7-x-1', 30, 2000, 2000, 60), extent=[0.4, 0.42, -0.01, 0.01], cmap='inferno')
plt.axis('off')
plt.show()
plt.close()

# for i in range(360, 365):
#   t = i
#   plt.imshow(newton_raphson_map('x^5-3x^4+9x^3+2x^2-x-1', 30, 2500, 2500, t), extent=[-10/(2**(t/30)) + 0.41187, 10/(2**(t/30)) + 0.41187, 10/(2**(t/30)), -10/(2**(t/30))], cmap='inferno')
#   plt.axis('off')
#   # plt.show()
#   plt.savefig('Newton_Raphson{0:03d}.png'.format(i), bbox_inches='tight', dpi=300)
#   plt.close()