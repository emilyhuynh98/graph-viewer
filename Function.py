from abc import ABC, abstractmethod
import numpy as np
import warnings

class Function(ABC):
	"""
	This is an abstract class that describes what other functions that extend from it should do.
	The only abstract method to be implemented by the 'concrete' classes is the y value.
	Otherwise, all classes similarly require a get_parameter and x_vals functions, which do not differ from class to class.
	"""
	def get_params(self,params):
		self.A = params[3]
		self.B = params[4]
		self.low_x = params[0]
		self.high_x = params[1]
		self.res = params[2]

	def x_vals(self):
		temp = np.arange(self.low_x, self.high_x + self.res, self.res)
		if temp[-1] > self.high_x:
			# If the last x element is greater than the maximum X (usually as a result of a large resolution),
			# replace the last element with the maximum x.
			temp[-1] = self.high_x
		elif temp[-1] < self.high_x:
			# If the resolution falls short of filling the specified range, manually add it in.
			temp = np.append(temp,self.high_x)
		return temp

	@abstractmethod
	def y(self):
		pass


class Sine(Function):
	"""
	Plots a sine function extended from the Function class.
	Extends the abstract Function class with optional parameters, and will otherwise default.
	General form of a Sine: Asin(Bx).
	"""
	def __init__(self,params=[-10,10,0.1,1,1]):
		self.get_params(params)
		self.name = 'Sine'
		self.gen = 'Asin(Bx)'
		self.x = self.x_vals()
		self.y = self.y()

	def y(self):
		self.y = self.A * np.sin(self.B * self.x)
		return self.y

class Sawtooth(Function):
	"""
	Plots a sine function extended from the Function class.
	Extends the abstract Function class with optional parameters, and will otherwise default.

	The sawtooth wave is an asymmetric triangle wave function, with a wavelength of 3 X-units.
	Notice that the up-slope is 1 X-unit long, and the down-slope is 2 X-units long.
	"""
	def __init__(self, params=[-10,10,0.1,1]):
		self.get_params(params)
		self.name = 'Sawtooth'
		self.gen = 'Vertical Scale: A, Vertical Shift: B'
		self.x = self.x_vals()
		self.y = self.y()

	def y(self):
		size = np.size(self.x)
		y = np.zeros(size)
		up_m = 1
		down_m = -0.5
		# m is the slope of up portion, calculated using (y2-y1)/(x2-x1).
		# Unscaled, unshifted points were interpolated from graph detailed in specs.
		# Points were: (0,-0.5) (1,0.5) (2,0) (3,-0.5) before applying parameters.
		i = 0
		for i in range(size):
			x_val = self.x[i]
			if x_val < 0:
				x_val = x_val % 3
			# If modulo 3 results in a value <= 1, then we are on the up-slope.
			# Therefore we graph the linear portion accordingly.
			if x_val % 3 <= 1:
				y[i] = self.A * (up_m * (x_val % 3) - 0.5)
			else:
				y[i] = self.A * (down_m * (x_val % 3) + 1)
		return y + self.B


class Exponential(Function):
	"""
	Plots an exponential function extended from the abstract Function class.
	"""

	def __init__(self,params=[-10,10,0.1,1,1]):
		self.get_params(params)
		self.name = 'Exponential'
		self.gen = 'Ax^B'
		self.x = self.x_vals()
		self.y = self.y()


	def y(self):
		y = self.A * (self.x**self.B)
		return y