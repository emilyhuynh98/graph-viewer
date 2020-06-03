from Plotter import GraphViewerUI
from Controller import Controller
from Function import Sine,Sawtooth,Exponential,Function
import numpy as np
import unittest

class testViewer(unittest.TestCase):
	def test_unit_sine(self):
		"""
		Tests that the Sine function outputs the correct values. Compares output against pre-calculated values.
		Uses A = 1, B = 1.
		"""
		x = np.arange(-10,10.1,0.1)
		calculated = np.sin(x).tolist()
		output = Sine().y
		output = output[:np.size(output)-1] # Have to slice off the last element, which is manually added in the code to meet max specified range.
		self.assertListEqual(calculated,output.tolist())

	def test_params_sine(self):
		"""
		Tests that the Sine function outputs the correct values. Compares output against pre-calculated values.
		Uses minX = -50, maxX = 50, res = 1, A = 5, B = 5.
		"""
		x = 5*np.arange(-50,51,1)
		calculated = 5*np.sin(x)
		output = Sine([-50,51,1,5,5]).y
		output = output[:np.size(output) - 1]
		self.assertListEqual(calculated.tolist(),output.tolist())

	def test_unit_exp(self):
		"""
		Tests that the Exponential function outputs the correct values. Compares output against pre-calculated values.
		Uses default params.
		"""
		x = np.arange(-10,10.1,0.1)
		calculated = x
		output = Exponential().y
		output = output[:np.size(output) - 1]
		self.assertListEqual(calculated.tolist(),output.tolist())

	def test_params_exp(self):
		"""
		Tests that the Sine function outputs the correct values. Compares output against pre-calculated values.
		Uses minX = -50, maxX = 50, res = 1, A = 5, B = 5.
		"""
		x = np.arange(-50,51,1)
		calculated = 5*(np.power(x,5))
		output = Exponential([-50,51,1,5,5]).y
		output = output[:np.size(output) - 1]
		self.assertListEqual(calculated.tolist(),output.tolist())

	def test_sqrt_exp(self):
		"""
		Tests that the Sine function outputs the correct values. Compares output against pre-calculated values.
		Uses minX = -10, maxX = 10, res = 0.1, A = 5, B = 1.5.
		"""
		c = Controller()
		c.currFcn = 'Exponential'
		c.curr_params = [0.01,10,0.1,5,1.5]
		output = c.plot_function('Exponential')
		x = np.arange(0.01,10.1,0.1)
		calculated = 5*(np.power(x,3/2))
		self.assertListEqual(np.round(calculated).tolist(),np.round(output).tolist())

	def test_21_sawtooth(self):
		"""
		Tests that Sawtooth with A = 2, B = 1 produces the correct points as given in the spec.
		Points are compared rather than a function.
		"""
		expected = [[-5,2],[-3,0],[-2,2],[0,0],[1,2],[3,0],[4,2]]
		actual = Sawtooth([-5,5,0.1,2,1]).y
		self.assertEqual(expected[0][1],actual[0])
		#Rounding for higher values as a result of float precision.
		self.assertEqual(expected[1][1],np.round(actual[20]))
		self.assertEqual(expected[2][1],np.round(actual[30]))
		self.assertEqual(expected[3][1],np.round(actual[50]))
		self.assertEqual(expected[4][1],np.round(actual[60]))
		self.assertEqual(expected[5][1],np.round(actual[80]))
		self.assertEqual(expected[6][1],np.round(actual[90]))

	def test_44_sawtooth(self):
		"""
		Tests that Sawtooth with A = 4, B = 4 produces the correct points as given in the spec.
		Points are compared rather than a function.
		"""
		expected = [[-3,2],[-2,6],[0,2],[1,6],[3,2],[4,6]]
		actual = Sawtooth([-5,5,0.1,4,4]).y
		self.assertEqual(expected[0][1],np.round(actual[20]))
		#Rounding for higher values as a result of float precision.
		self.assertEqual(expected[1][1],np.round(actual[30]))
		self.assertEqual(expected[2][1],np.round(actual[50]))
		self.assertEqual(expected[3][1],np.round(actual[60]))
		self.assertEqual(expected[4][1],np.round(actual[80]))
		self.assertEqual(expected[5][1],np.round(actual[90]))

	def test_string_inputs(self):
		"""
		Mimics String inputs to QLineEdit to check if errors are picked up.
		"""
		c = Controller()
		self.assertEqual(c.is_valid(['a',5,3,'b',1]),False)
		self.assertEqual(c.is_valid([5,'a',3,3,1]),False)
		self.assertEqual(c.is_valid([5,'a','b',2,1]),False)
		self.assertEqual(c.is_valid([5,'a','b',2,1]),False)
		self.assertEqual(c.is_valid(['5','a','b',2,1]),False)

	def test_rangeX_params(self):
		"""
		Mimics inputs to QLineEdit to check if errors are picked up.
		Checks if max X <= min X returns errors.
		Checks if X is too large, if it will return errors.
		"""
		c = Controller()
		self.assertEqual(c.is_valid([-10,-20,1,1,1]),True)
		self.assertEqual(c.is_valid([-10000,-20,1,1,1]),False)
		self.assertEqual(c.is_valid([-10,-10000,1,1,1]),False)

	def test_res_params(self):
		"""
		Mimics inputs to QLineEdit to check if errors are picked up.
		Checks if res > span(X)/2, returns error.
		"""
		c = Controller()
		self.assertEqual(c.is_valid([-5,5,7,1,1]), False)

	def Linear(self):
		"""
		"Added" function in for testAddFunction with A = 5, B = 3.
		"""
		func = Function('linear',[-10,10,0.1,5,3])
		gen = 'Ax+B'
		x = func.x_vals()
		y = func.A * x + func.B
		return y[:np.size(y)-1]

	def testAddFunction(self):
		"""
		Tests if adding functions can be done correctly.
		"""
		test_function = self.Linear()
		test_x = np.arange(-10,10.1,0.1)
		expected = 5 * test_x + 3
		self.assertListEqual(expected.tolist(),test_function.tolist())



def main():
	testViewer()



if __name__ == '__main__':
	unittest.main()

