﻿# GraphViewer ReadMe

## Instructions to Run
**Required dependencies:** Python3, PyQt5, PyQtGraph, NumPy. Tested on MacOS.

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
class Linear(object):
	"""
	Plots an linear function extended from the Function class.
	"""

	def __init__(self,params=[-10,10,0.1,1,1]):
		self.func = Function('linear',params)
		self.x = self.func.x_vals()
		self.gen = 'Ax+B'
		self.y = self.y()


	def y(self):
		y = self.func.A * self.x + self.func.B
		return y
```
Extending from the Function class will generate the range of x-values expected by the specified or default parameters. 

 - The Function class is initialized as follows:
``Function(Str function_name, List params)``.
 - ``self.gen`` is used to describe what the general form of the function does. This helps the user understand what ``A`` and ``B`` does.
 - ``def y(self)`` is where the function is actually defined.

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
 - Working new function creation

## How it works
The GraphViewer allows the user to plot three basic pre-selected functions, and adjust the X range, resolution, as well as A and B parameters.

It is implemented using a Model-View-Controller (MVC) design (see [figure](https://commons.wikimedia.org/wiki/File:MVC-Process.svg#/media/File:MVC-Process.svg) below).
![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MVC-Process.svg/1280px-MVC-Process.svg.png)
The MVC divides the full stack up into three elements that interact. The Model is the back-end. In this case, this consists of the functions held in ``Function.py``. The view is the GUI, which is what the user sees. The GUI is held in ``Plotter.py`` and is implemented using PyQt5 and PyQtGraph. The Controller (``Controller.py``) reads signals emitted from the GUI and connects it to actions (e.g., selecting a function will plot the function accordingly).

