import numpy as np
import warnings

class Function(object):
	"""
	This class defines a Function object. 

	The goal of the Function object is to define its attributes (scaling/shifting factors, function name). 
	"""

	def __init__(self, name, params):
		"""
		Parameters:
		name: String type. User-defined name. 
		A: Float. User-defined constant. Scales graph. Default A = 1.
		B: Float. User-defined constant. Shifts graph. Default B = 1.
		low_x: 
		high_x:
		res:
		"""
		self.A = params[3]
		self.B = params[4]
		self.name = name
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


class Sine(object):
	"""
	Plots a sine function extended from the Function class.
	Initializes as a Function object with optional parameters, and will otherwise default.
	General form of a Sine: Asin(Bx).
	"""
	def __init__(self,params=[-10,10,0.1,1,1]):
		self.func = Function('sine',params)
		self.gen = 'Asin(Bx)'
		self.x = self.func.x_vals()
		self.y = self.y()

	def y(self):
		self.y = self.func.A * np.sin(self.func.B * self.x)
		return self.y

class Sawtooth(object):
	"""
	Plots a sine function extended from the Function class.
	Initializes as a Function object with optional parameters, and will otherwise default.

	The sawtooth wave is an asymmetric triangle wave function, with a wavelength of 3 X-units.
	Notice that the up-slope is 1 X-unit long, and the down-slope is 2 X-units long.
	"""
	def __init__(self, params=[-10,10,0.1,1]):
		self.func = Function('sawtooth',params)
		self.gen = 'Vertical Scale: A, Vertical Shift: B'
		self.x = self.func.x_vals()
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
				y[i] = self.func.A * (up_m * (x_val % 3) - 0.5)
			else:
				y[i] = self.func.A * (down_m * (x_val % 3) + 1)
		return y + self.func.B


class Exponential(object):
	"""
	Plots an exponential function extended from the Function class.
	"""

	def __init__(self,params=[-10,10,0.1,1,1]):
		self.func = Function('exponential',params)
		self.x = self.func.x_vals()
		self.gen = 'Ax^B'
		self.y = self.y()


	def y(self):
		y = self.func.A * (self.x**self.func.B)
		return y