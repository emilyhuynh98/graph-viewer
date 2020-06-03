import sys
from PyQt5.QtWidgets import QHBoxLayout,QMessageBox,QGridLayout,QPushButton,QVBoxLayout,QApplication,QWidget,QLabel,QComboBox,QLineEdit
from pyqtgraph import plot
import pyqtgraph as pg
import numpy as np

class GraphViewerUI(QWidget):
	"""
	The Plotter class implements the GUI. In doing so, it receives user actions and events, which are sent to the Controller.
	Includes methods for user-selectable range, viewing pointers, setting colors of plots, legends, etc.s
	"""
	def __init__(self, *args, **kwargs):
		super(GraphViewerUI, self).__init__(*args, **kwargs)
		self.functions = [" ","Sine", "Sawtooth", "Exponential"]

		# Sets up the layout of the widgets (stacks vertically)
		self.hLayout = QVBoxLayout(self)
		self.setWindowTitle("Graph Viewer")

		# Sets up the graph viewer widget
		pg.setConfigOption('background','w')
		self.graphWindow = pg.GraphicsWindow(title="Window")
		self.hLayout.addWidget(self.graphWindow)

		# Sets up the function selection widget
		self.create_dropdown()

		# Sets up adjustable parameters
		self.create_grid()

	def _graph(self):
		return self.graphWindow

	def create_dropdown(self):
		"""
		Creates dropdown menu, where user can select a function to plot.
		"""
		layout = QVBoxLayout()
		self.cb = QComboBox()
		self.cb.addItems(self.functions)
		layout.addWidget(self.cb)
		self.hLayout.addLayout(layout)

	def create_grid(self):
		"""
		Creates grid to include adjustable parameters.
		"""
		self.minXlabel = QLabel('Min X:')
		self.maxXlabel = QLabel('Max X:')
		self.resXlabel = QLabel('Res X:')
		self.Alabel = QLabel('A:')
		self.Blabel = QLabel('B:')
		self.minX = QLineEdit(self)
		self.maxX = QLineEdit(self)
		self.resX = QLineEdit(self)
		self.A = QLineEdit(self)
		self.B = QLineEdit(self)
		self.button = QPushButton('Apply', self)

		labels = [self.minXlabel, self.maxXlabel,self.resXlabel,self.Alabel,self.Blabel]
		self.params = [self.minX,self.maxX,self.resX,self.A,self.B]

		grid = QGridLayout()
		grid.setSpacing(10)

		for i in range(np.size(labels)):
			grid.addWidget(labels[i], 1, i)
			grid.addWidget(self.params[i], 2, i)
		grid.addWidget(self.button,2,5)
		self.hLayout.addLayout(grid)