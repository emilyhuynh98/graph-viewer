# GraphViewer ReadMe

## Instructions to Run
**Required dependencies:** PyQt5, PyQtGraph, NumPy. Tested on MacOS using Python 3.

These dependencies can be installed via ``pip install [dependency]``.

Once installed, open terminal and ``cd`` into folder. 

Run ``python main.py`` to run the GraphViewer. 
Run ``python test.py`` to run unit tests.

The three viewable functions are: Sinusoidal, Sawtooth, and Exponential.

## Adding/Modifying Functions

### Adding a function
#### Step 1. Add to ``Function.py`` 
To add a function, open ``Function.py``. At the end of the file, add your function similarly to the other functions.

For example, to create a Linear class extended from abstract base class Function:
```Python
class Linear(Function):
	"""
	Plots an linear function extended from the abstract Function class.
	"""

	def __init__(self,params=[-10,10,0.1,1,1]):
		self.get_params(params)
		self.name = 'Linear'
		self.gen = 'Ax+B'
		self.x = self.x_vals()
		self.y = self.y()

	def y(self):
		y = self.A * self.x + self.B
		return y
```
Extending from the Function class will generate the range of x-values expected by the specified or default parameters. 

 - The abstract Function class is as follows:
 - ``def get_params(self,params)`` and ``def x_vals(self)``is defined the same for every function.
 - ``def y(self)`` is the only method that must be defined by each class (@abstractmethod.)

#### Step 2. Add it to the list of functions.
Open ``Plotter.py`` , and on line 15, add your ``function_name`` to the list.
e.g.,
```Python
self.functions = [" ","Sine", "Sawtooth", "Exponential", "Linear"]
```

#### Step 3. Link the function name to the function itself.
Open ``Controller.py`` and in between lines 85-104, add
```Python
elif fcn == 'Linear'
	to_plot = Linear(self.curr_params) 
```
At the top of the file, on line 4, add Linear:
```Python
from Function import Sine,Sawtooth,Exponential,Linear
```
Saving all these files and running ``python main.py`` again to open a new window will show your new function!

### Modifying an existing function
To modify how an existing function works, simply go to ``Function.py``, scroll to the existing function's class, and edit the function ``def y(self)`` accordingly.


## Test Cases
The basic test cases from `test.py` include 

 - Standard function outputs, with/without various parameters adjusted
 - Properly ordered X range
 - Parameter limits
 - Appropriate x resolution
 - Type checking input parameters

## How it works
The GraphViewer allows the user to plot three basic pre-selected functions, and adjust the X range, resolution, as well as A and B parameters.

It is implemented using a Model-View-Controller (MVC) design (see [figure](https://commons.wikimedia.org/wiki/File:MVC-Process.svg#/media/File:MVC-Process.svg) below).
![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MVC-Process.svg/1280px-MVC-Process.svg.png)
The MVC divides the full stack up into three elements that interact. The Model is the back-end. In this case, this consists of the functions held in ``Function.py``. The view is the GUI, which is what the user sees. The GUI is held in ``Plotter.py`` and is implemented using PyQt5 and PyQtGraph. The Controller (``Controller.py``) reads signals emitted from the GUI and connects it to actions (e.g., selecting a function will plot the function accordingly).


