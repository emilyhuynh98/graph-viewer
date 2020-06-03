import sys
import numpy as np
from Plotter import GraphViewerUI
from Function import Sine,Sawtooth,Exponential
from PyQt5.QtWidgets import QHBoxLayout,QMessageBox,QGridLayout,QPushButton,QVBoxLayout,QApplication,QWidget,QLabel,QComboBox,QLineEdit
from pyqtgraph import plot
import pyqtgraph as pg

class Controller:
	"""
	Controller class, to connect the GUI (Plotter.py) with the model (Function.py)
	"""
	def __init__(self):
		self.app = QApplication(sys.argv)
		# Import GUI
		self.view = GraphViewerUI()
		self.currFcn = ''
		self.cb = self.view.cb
		self.button = self.view.button
		self.qline = self.view.params

		# Variable to store parameters in case of error
		# Set to the default initial values: [minX, maxX, resX, A, B]
		self.curr_params = [-10,10,0.1,1,1]

		# Access dropdown menu items (the functions) from GUI
		self.connect_signals()

	def run(self):
		"""
		Runs the GUI. 
		"""
		self.view.show()
		return self.app.exec_()

	def connect_signals(self):
		# Connects: selecting function from dropdown menu to update_plot
		self.cb.activated.connect(self.update_plot)

		for elem in self.qline:
			elem.returnPressed.connect(self.update_params)

		# Connects: clicking apply button to update_params
		self.button.clicked.connect(self.update_params)

	def update_plot(self):
		new_fcn = self.cb.currentText()

		# Grabs current parameters for plot, for when it has errored out.
		self.set_to_prev()

		# Plots function
		self.plot_function(new_fcn)

	def update_params(self):
		"""
		Grabs new parameter values from QLineEdit boxes and checks if valid before applying to function.
		If invalid, discards values and keeps previous values.
		"""
		params_temp = [self.view.minX.text(),self.view.maxX.text(),self.view.resX.text(),self.view.A.text(),self.view.B.text()]
		if self.is_valid(params_temp):
			for i in range(np.size(params_temp)):
				self.curr_params[i] = float(params_temp[i])
			self.update_plot()


	def set_to_prev(self):
		# Set QLineEdits (min,max,res, A,B) to original parameters
		self.view.minX.setText(str(self.curr_params[0]))
		self.view.maxX.setText(str(self.curr_params[1]))
		self.view.resX.setText(str(self.curr_params[2]))
		self.view.A.setText(str(self.curr_params[3]))
		self.view.B.setText(str(self.curr_params[4]))

	def plot_function(self,fcn):
		"""
		Plots function selected in dropdown menu. Will reset parameters for each selection (including if same selection).
		"""
		if self.currFcn != fcn:
			self.currFcn = fcn
			# If plotting a new function, reset parameters.
			self.curr_params = [-10,10,0.1,1,1]
			self.set_to_prev()

		if fcn == 'Sine':
			to_plot = Sine(self.curr_params)
		elif fcn == 'Sawtooth':
			to_plot = Sawtooth(self.curr_params)
		elif fcn == 'Exponential':
			to_plot = Exponential(self.curr_params)
			# If B is a negative whole number, then the asymptotes are addressed as two separate plots.
			# Temp is used to find if we will find an asymptote (if it is negative, then we cross the origin).
			# If so, we split into two arrays near 0.
			temp = self.curr_params[0] * self.curr_params[1]
			if self.curr_params[4] < 0 and temp < 0:
				neg_y,neg_x,pos_y,pos_x = self.split_asymptote(to_plot)
				self.view._graph().clear()
				self.plt = self.view._graph().addPlot()
				titleStyle = {'color': '#adadad', 'size': '18pt'}
				self.plt.setTitle(fcn + ": "  + to_plot.gen,**titleStyle)
				pen = pg.mkPen(color=(255,0,0),width=5)
				self.plt.plot(neg_x, neg_y, pen=pen)
				self.plt.plot(pos_x, pos_y, pen=pen)
				return
		elif fcn == ' ':
			self.view._graph().clear()
			return

		# Clears the graphics window of any previous plots
		self.view._graph().clear()

		# Adds new plot to the graphics window
		self.plt = self.view._graph().addPlot()
		titleStyle = {'color': '#adadad', 'size': '18pt'}
		self.plt.setTitle(fcn + ": "  + to_plot.gen,**titleStyle)
		pen = pg.mkPen(color=(255,0,0),width=5)
		self.plt.plot(to_plot.x, to_plot.y, pen=pen)
		return to_plot.y

	def split_asymptote(self,to_plot):
		"""
		Used when encountering an asymptotic function (Exponential with B < 0 and B % 1 == 0).
		Arbitrarily splits the array near the asymptote (x=0) to plot appropriately.
		"""
		neg_ind = int(np.abs((self.curr_params[0] + 0.5) / (self.curr_params[2])))
		neg_y = to_plot.y[:neg_ind+1]
		neg_x = to_plot.x[:neg_ind+1]
		pos_ind = int(np.abs((self.curr_params[0] - 0.5)/(self.curr_params[2])))
		pos_y = to_plot.y[pos_ind+1:]
		pos_x = to_plot.x[pos_ind+1:]
		return neg_y,neg_x,pos_y,pos_x


	def is_valid(self,params):
		"""
		Checks if changed parameters are valid.
		Test 1. Correct type (float)
		Test 2. min X < max X.
		Test 3. res X > 0.
		Test 4. res X is such that at least two points can be plotted.
		"""
		for i in range(np.size(params)):
			try:
				params[i] = float(params[i])
			except ValueError:
				msg = params[i] + " is not type int or float. Returning to previous parameters."
				self.error_msg(msg)
				self.set_to_prev()
				return False
			i += 0

		# Checking limits on min X and max X:
		if params[0] > params[1]:
			msg = "min X is greater than max X. Returning to previous parameters."
			self.error_msg(msg)
			self.set_to_prev()
			return False

		elif params[0] == params[1]:
			msg = "min X is equal to max X. Returning to previous parameters."
			self.error_msg(msg)
			self.set_to_prev()
			return False

		# Checking min X value limit to prevent too many calculations/timeout/memory error.
		if np.abs(params[0] - params[1]) > 1000:
			msg = "X range is too large. Returning to previous parameters."
			self.error_msg(msg)
			self.set_to_prev()
			return False

		# Checking non-negative value for resolution. 
		# Implementing that resolution be > 0.001 for calculation purposes.
		elif params[2] <= 0 or params[2] < 0.001:
			msg = "Negative or too small resolution value (min 0.001). Returning to previous parameters."
			self.error_msg(msg)
			self.set_to_prev()
			return False

		# Checking limits of res to make sure res < half-span of X:
		elif params[2] > np.abs(params[1] - params[0])/2:
			msg = "Resolution is too large for this range. Must be able to plot two data points within range. Returning to previous parameters."
			self.error_msg(msg)
			self.set_to_prev()
			return False

		# Checking that resolution is adeuqate for exponential functions that contain an asymptote.
		# Imposed requirement on resolution due to approximation of array slicing around the asymptote.
		elif params[2] > np.abs(params[1] - params[0])/6.5 and self.currFcn == 'Exponential' and params[4] < 0 and params[4] % 1 == 0:
			msg = "Resolution is too large for this range. Must be able to plot two data points within range. Returning to previous parameters."
			self.error_msg(msg)
			self.set_to_prev()
			return False

		# Checking that min X  >= 0 when exponential results in a square root, which would have imaginary numbers if negative.
		elif params[4] % 1 != 0 and params[0] < 0 and self.currFcn == 'Exponential':
			params[0] = 0.01
			self.error_msg("min X < 0 for square roots is invalid. Changing minimum X to 0.01.")
			self.set_to_prev()			

		return True

	def error_msg(self,msg):
		# Sends error message to user.
		error = QMessageBox()
		error.setIcon(QMessageBox.Warning)
		error.setText("Error: "+ msg)
		error.setWindowTitle("GraphViewer Error")
		error.setStandardButtons(QMessageBox.Ok)
		error.exec_()